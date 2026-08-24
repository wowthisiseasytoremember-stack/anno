//  AudioDevotionalPlayer.swift
//  Anno
//
//  Production audio player service managing high-fidelity sacred audio narration,
//  AVFoundation background audio session, lock-screen media controls (MPNowPlayingInfoCenter &
//  MPRemoteCommandCenter), speed adjustments, sleep timer, and bilingual audio switching.

import Foundation
import AVFoundation
import MediaPlayer
import Combine
import SwiftUI

// MARK: - Audio Devotional Player Service

@MainActor
public final class AudioDevotionalPlayer: ObservableObject {
    public static let shared = AudioDevotionalPlayer()

    // MARK: - Published State
    @Published public private(set) var catalog: [AudioNarrationTrack] = []
    @Published public private(set) var currentTrack: AudioNarrationTrack? = nil
    @Published public private(set) var isPlaying: Bool = false
    @Published public private(set) var isBuffering: Bool = false
    @Published public private(set) var currentTime: TimeInterval = 0
    @Published public private(set) var duration: TimeInterval = 0
    @Published public private(set) var playbackSpeed: PlaybackSpeedOption = .speed1_0x
    @Published public private(set) var sleepTimerOption: SleepTimerOption = .off
    @Published public private(set) var sleepTimerRemainingSeconds: TimeInterval? = nil
    @Published public private(set) var activeLanguage: LanguageMode = .english
    @Published public var errorMessage: String? = nil

    // MARK: - Internal Player Properties
    private var player: AVPlayer? = nil
    private var playerItem: AVPlayerItem? = nil
    private var timeObserverToken: Any? = nil
    private var statusObserver: NSKeyValueObservation? = nil
    private var bufferEmptyObserver: NSKeyValueObservation? = nil
    private var likelyToKeepUpObserver: NSKeyValueObservation? = nil
    private var cancellables = Set<AnyCancellable>()

    // Sleep Timer
    private var sleepTimerTask: Task<Void, Never>? = nil

    // Mock Mode
    public var isMockMode: Bool = false

    // MARK: - Initialization

    public init(isMockMode: Bool = false) {
        self.isMockMode = isMockMode
        if !isMockMode {
            configureAudioSession()
            setupRemoteCommands()
            setupNotificationObservers()
            loadCatalog()
        }
    }

    deinit {
        // Cleanup resources
        if let token = timeObserverToken, let p = player {
            p.removeTimeObserver(token)
        }
        statusObserver?.invalidate()
        bufferEmptyObserver?.invalidate()
        likelyToKeepUpObserver?.invalidate()
        sleepTimerTask?.cancel()
    }

    // MARK: - Catalog Loading

    public func loadCatalog(bundle: Bundle = .main) {
        guard let url = bundle.url(forResource: "audio_narration_catalog", withExtension: "json") else {
            return
        }
        do {
            let data = try Data(contentsOf: url)
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            let decoded = try decoder.decode(AudioNarrationCatalog.self, from: data)
            self.catalog = decoded.tracks
        } catch {
            print("Failed to load audio narration catalog: \(error)")
        }
    }

    // MARK: - Audio Session Configuration

    private func configureAudioSession() {
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(
                .playback,
                mode: .spokenAudio,
                options: [.allowAirPlay, .allowBluetooth, .allowBluetoothA2DP]
            )
            try session.setActive(true)
        } catch {
            print("Failed to configure AVAudioSession: \(error)")
        }
    }

    // MARK: - Playback Control Methods

    public func play(track: AudioNarrationTrack, language: LanguageMode = .english, startTime: TimeInterval = 0) {
        self.currentTrack = track
        self.activeLanguage = language
        self.duration = track.durationSeconds
        self.currentTime = startTime
        self.errorMessage = nil

        if isMockMode {
            self.isPlaying = true
            self.isBuffering = false
            return
        }

        guard let streamURL = track.audioURL(for: language) else {
            self.errorMessage = "Invalid audio stream URL."
            return
        }

        cleanupCurrentItem()

        let asset = AVURLAsset(url: streamURL)
        let item = AVPlayerItem(asset: asset)
        self.playerItem = item

        if player == nil {
            player = AVPlayer(playerItem: item)
            setupPeriodicTimeObserver()
        } else {
            player?.replaceCurrentItem(with: item)
        }

        observePlayerItem(item)

        if startTime > 0 {
            let targetCM = CMTime(seconds: startTime, preferredTimescale: 600)
            player?.seek(to: targetCM, toleranceBefore: .zero, toleranceAfter: .zero)
        }

        player?.rate = playbackSpeed.rawValue
        self.isPlaying = true
        self.isBuffering = true

        updateNowPlayingInfo()
    }

    public func togglePlayPause() {
        if isPlaying {
            pause()
        } else {
            resume()
        }
    }

    public func pause() {
        guard isPlaying else { return }
        player?.pause()
        isPlaying = false
        isBuffering = false
        updateNowPlayingPlaybackState()
    }

    public func resume() {
        guard !isPlaying else { return }
        guard let currentTrack = currentTrack else {
            if let first = catalog.first {
                play(track: first, language: activeLanguage)
            }
            return
        }

        if player == nil {
            play(track: currentTrack, language: activeLanguage, startTime: currentTime)
            return
        }

        player?.rate = playbackSpeed.rawValue
        isPlaying = true
        updateNowPlayingPlaybackState()
    }

    public func stop() {
        pause()
        seek(to: 0)
        currentTrack = nil
        clearNowPlayingInfo()
    }

    public func seek(to seconds: TimeInterval) {
        let clampedSeconds = max(0, min(seconds, duration > 0 ? duration : seconds))
        self.currentTime = clampedSeconds

        if !isMockMode {
            let targetCM = CMTime(seconds: clampedSeconds, preferredTimescale: 600)
            player?.seek(to: targetCM, toleranceBefore: .zero, toleranceAfter: .zero)
            updateNowPlayingInfo()
        }
    }

    public func skipForward(seconds: Double = 15.0) {
        seek(to: currentTime + seconds)
    }

    public func skipBackward(seconds: Double = 15.0) {
        seek(to: currentTime - seconds)
    }

    public func setPlaybackSpeed(_ speed: PlaybackSpeedOption) {
        self.playbackSpeed = speed
        if isPlaying && !isMockMode {
            player?.rate = speed.rawValue
            updateNowPlayingPlaybackState()
        }
    }

    public func setLanguage(_ language: LanguageMode) {
        guard language != self.activeLanguage else { return }
        let currentPos = self.currentTime
        let wasPlaying = self.isPlaying
        self.activeLanguage = language

        guard let track = self.currentTrack else { return }

        if wasPlaying {
            play(track: track, language: language, startTime: currentPos)
        } else {
            // Pre-load at current position without auto-starting if paused
            self.currentTime = currentPos
            if let streamURL = track.audioURL(for: language) {
                cleanupCurrentItem()
                let item = AVPlayerItem(url: streamURL)
                self.playerItem = item
                player?.replaceCurrentItem(with: item)
                observePlayerItem(item)
                let targetCM = CMTime(seconds: currentPos, preferredTimescale: 600)
                player?.seek(to: targetCM, toleranceBefore: .zero, toleranceAfter: .zero)
                updateNowPlayingInfo()
            }
        }
    }

    public func seekToCuePoint(_ cuePoint: AudioCuePoint) {
        seek(to: cuePoint.timeSeconds)
    }

    // MARK: - Sleep Timer

    public func setSleepTimer(_ option: SleepTimerOption) {
        self.sleepTimerOption = option
        sleepTimerTask?.cancel()
        sleepTimerTask = nil

        switch option {
        case .off:
            self.sleepTimerRemainingSeconds = nil

        case .minutes(let minutes):
            let totalSecs = TimeInterval(minutes * 60)
            self.sleepTimerRemainingSeconds = totalSecs
            startSleepTimerCountdown(totalSeconds: totalSecs)

        case .endOfTrack:
            let remaining = max(0, duration - currentTime)
            self.sleepTimerRemainingSeconds = remaining
            // Handled when track ends in itemDidPlayToEnd
        }
    }

    private func startSleepTimerCountdown(totalSeconds: TimeInterval) {
        sleepTimerTask = Task { [weak self] in
            var remaining = totalSeconds
            while remaining > 0 {
                try? await Task.sleep(nanoseconds: 1_000_000_000)
                if Task.isCancelled { return }
                guard let self = self else { return }
                remaining -= 1
                self.sleepTimerRemainingSeconds = max(0, remaining)
            }

            // Timer expired
            if let self = self {
                self.pause()
                self.sleepTimerOption = .off
                self.sleepTimerRemainingSeconds = nil
            }
        }
    }

    // MARK: - Item Observers & Lifecycle

    private func setupPeriodicTimeObserver() {
        let interval = CMTime(seconds: 0.25, preferredTimescale: 600)
        timeObserverToken = player?.addPeriodicTimeObserver(forInterval: interval, queue: .main) { [weak self] time in
            guard let self = self, !self.isMockMode else { return }
            let secs = time.seconds
            if !secs.isNaN && !secs.isInfinite {
                self.currentTime = secs
            }
        }
    }

    private func observePlayerItem(_ item: AVPlayerItem) {
        statusObserver?.invalidate()
        bufferEmptyObserver?.invalidate()
        likelyToKeepUpObserver?.invalidate()

        statusObserver = item.observe(\.status, options: [.new]) { [weak self] observedItem, _ in
            Task { @MainActor [weak self] in
                guard let self = self else { return }
                switch observedItem.status {
                case .readyToPlay:
                    self.isBuffering = false
                    let itemDuration = observedItem.duration.seconds
                    if !itemDuration.isNaN && !itemDuration.isInfinite && itemDuration > 0 {
                        self.duration = itemDuration
                    }
                    self.updateNowPlayingInfo()
                case .failed:
                    self.isBuffering = false
                    self.isPlaying = false
                    self.errorMessage = observedItem.error?.localizedDescription ?? "Playback failed."
                case .unknown:
                    break
                @unknown default:
                    break
                }
            }
        }

        bufferEmptyObserver = item.observe(\.isPlaybackBufferEmpty, options: [.new]) { [weak self] observedItem, _ in
            Task { @MainActor [weak self] in
                guard let self = self else { return }
                if observedItem.isPlaybackBufferEmpty {
                    self.isBuffering = true
                }
            }
        }

        likelyToKeepUpObserver = item.observe(\.isPlaybackLikelyToKeepUp, options: [.new]) { [weak self] observedItem, _ in
            Task { @MainActor [weak self] in
                guard let self = self else { return }
                if observedItem.isPlaybackLikelyToKeepUp {
                    self.isBuffering = false
                }
            }
        }
    }

    private func cleanupCurrentItem() {
        statusObserver?.invalidate()
        statusObserver = nil
        bufferEmptyObserver?.invalidate()
        bufferEmptyObserver = nil
        likelyToKeepUpObserver?.invalidate()
        likelyToKeepUpObserver = nil
    }

    // MARK: - Notifications (Interruptions, Route Changes, End of Track)

    private func setupNotificationObservers() {
        NotificationCenter.default.publisher(for: .AVPlayerItemDidPlayToEndTime)
            .receive(on: DispatchQueue.main)
            .sink { [weak self] notification in
                self?.handleTrackEnded(notification)
            }
            .store(in: &cancellables)

        NotificationCenter.default.publisher(for: AVAudioSession.interruptionNotification)
            .receive(on: DispatchQueue.main)
            .sink { [weak self] notification in
                self?.handleAudioInterruption(notification)
            }
            .store(in: &cancellables)

        NotificationCenter.default.publisher(for: AVAudioSession.routeChangeNotification)
            .receive(on: DispatchQueue.main)
            .sink { [weak self] notification in
                self?.handleAudioRouteChange(notification)
            }
            .store(in: &cancellables)
    }

    private func handleTrackEnded(_ notification: Notification) {
        if sleepTimerOption == .endOfTrack {
            pause()
            setSleepTimer(.off)
            seek(to: 0)
            return
        }

        // Loop back to start or pause
        pause()
        seek(to: 0)
    }

    private func handleAudioInterruption(_ notification: Notification) {
        guard let userInfo = notification.userInfo,
              let typeValue = userInfo[AVAudioSessionInterruptionTypeKey] as? UInt,
              let type = AVAudioSession.InterruptionType(rawValue: typeValue) else {
            return
        }

        switch type {
        case .began:
            pause()
        case .ended:
            guard let optionsValue = userInfo[AVAudioSessionInterruptionOptionKey] as? UInt else { return }
            let options = AVAudioSession.InterruptionOptions(rawValue: optionsValue)
            if options.contains(.shouldResume) {
                resume()
            }
        @unknown default:
            break
        }
    }

    private func handleAudioRouteChange(_ notification: Notification) {
        guard let userInfo = notification.userInfo,
              let reasonValue = userInfo[AVAudioSessionRouteChangeReasonKey] as? UInt,
              let reason = AVAudioSession.RouteChangeReason(rawValue: reasonValue) else {
            return
        }

        if reason == .oldDeviceUnavailable {
            // Headphones were disconnected
            pause()
        }
    }

    // MARK: - Lock Screen Remote Media Commands

    private func setupRemoteCommands() {
        let commandCenter = MPRemoteCommandCenter.shared()

        commandCenter.playCommand.addTarget { [weak self] _ in
            Task { @MainActor [weak self] in
                self?.resume()
            }
            return .success
        }

        commandCenter.pauseCommand.addTarget { [weak self] _ in
            Task { @MainActor [weak self] in
                self?.pause()
            }
            return .success
        }

        commandCenter.togglePlayPauseCommand.addTarget { [weak self] _ in
            Task { @MainActor [weak self] in
                self?.togglePlayPause()
            }
            return .success
        }

        commandCenter.skipForwardCommand.preferredIntervals = [15.0]
        commandCenter.skipForwardCommand.addTarget { [weak self] event in
            guard let skipEvent = event as? MPSkipIntervalCommandEvent else { return .commandFailed }
            Task { @MainActor [weak self] in
                self?.skipForward(seconds: skipEvent.interval)
            }
            return .success
        }

        commandCenter.skipBackwardCommand.preferredIntervals = [15.0]
        commandCenter.skipBackwardCommand.addTarget { [weak self] event in
            guard let skipEvent = event as? MPSkipIntervalCommandEvent else { return .commandFailed }
            Task { @MainActor [weak self] in
                self?.skipBackward(seconds: skipEvent.interval)
            }
            return .success
        }

        commandCenter.changePlaybackPositionCommand.addTarget { [weak self] event in
            guard let positionEvent = event as? MPChangePlaybackPositionCommandEvent else { return .commandFailed }
            Task { @MainActor [weak self] in
                self?.seek(to: positionEvent.positionTime)
            }
            return .success
        }

        commandCenter.changePlaybackRateCommand.supportedPlaybackRates = [0.75, 1.0, 1.25, 1.5, 2.0]
        commandCenter.changePlaybackRateCommand.addTarget { [weak self] event in
            guard let rateEvent = event as? MPChangePlaybackRateCommandEvent,
                  let speed = PlaybackSpeedOption(rawValue: rateEvent.playbackRate) else {
                return .commandFailed
            }
            Task { @MainActor [weak self] in
                self?.setPlaybackSpeed(speed)
            }
            return .success
        }
    }

    // MARK: - Now Playing Info Center

    private func updateNowPlayingInfo() {
        guard let track = currentTrack else {
            clearNowPlayingInfo()
            return
        }

        var info: [String: Any] = [:]
        info[MPMediaItemPropertyTitle] = track.title(for: activeLanguage)
        info[MPMediaItemPropertyArtist] = "\(track.narrator(for: activeLanguage)) • \(track.sacredMusicBackground)"
        info[MPMediaItemPropertyAlbumTitle] = "Anno — Sacred History & Devotion"
        info[MPNowPlayingInfoPropertyElapsedPlaybackTime] = currentTime
        info[MPMediaItemPropertyPlaybackDuration] = duration > 0 ? duration : track.durationSeconds
        info[MPNowPlayingInfoPropertyPlaybackRate] = isPlaying ? Double(playbackSpeed.rawValue) : 0.0

        MPNowPlayingInfoCenter.default().nowPlayingInfo = info
    }

    private func updateNowPlayingPlaybackState() {
        guard var info = MPNowPlayingInfoCenter.default().nowPlayingInfo else {
            updateNowPlayingInfo()
            return
        }
        info[MPNowPlayingInfoPropertyElapsedPlaybackTime] = currentTime
        info[MPNowPlayingInfoPropertyPlaybackRate] = isPlaying ? Double(playbackSpeed.rawValue) : 0.0
        MPNowPlayingInfoCenter.default().nowPlayingInfo = info
    }

    private func clearNowPlayingInfo() {
        MPNowPlayingInfoCenter.default().nowPlayingInfo = nil
    }
}

// MARK: - Preview Mock Provider

extension AudioDevotionalPlayer {
    public static var preview: AudioDevotionalPlayer {
        let player = AudioDevotionalPlayer(isMockMode: true)
        let sampleTrack = AudioNarrationTrack(
            audioId: "audio-2026-07-03-thomas-apostle",
            date: "2026-07-03",
            liturgicalDay: "Feast of Saint Thomas, Apostle",
            feastRank: "Feast",
            titleEn: "Saint Thomas the Apostle: From Wounded Doubt to Unwavering Confession",
            titleVi: "Thánh Tôma Tông Đồ: Từ Nghi Ngờ Vết Thương Đến Lời Tuyên Xưng Sắt Son",
            audioUrlEn: "https://cdn.annoapp.com/audio/en/2026-07-03-thomas.m4a",
            audioUrlVi: "https://cdn.annoapp.com/audio/vi/2026-07-03-thomas.m4a",
            durationSeconds: 384,
            narratorName: "Rev. Benedict Marie, O.P.",
            narratorNameVi: "Lm. Giuse Maria Nguyễn Văn Bình",
            sacredMusicBackground: "Gregorian Chant (Mode IV - Salve Regina & Ubi Caritas)",
            musicLicenseInfo: "Public Domain Liturgical Chant",
            transcriptEn: "In the Name of the Father, and of the Son, and of the Holy Spirit. Amen. Today the Church celebrates Saint Thomas, the Apostle of India, who dared to bring his wounded doubt into the presence of the Risen Christ...",
            transcriptVi: "Nhân danh Cha và Con và Thánh Thần. Amen. Hôm nay Hội Thánh cử hành lễ kính Thánh Tôma, Vị Tông Đồ của Ấn Độ, người đã can đảm mang sự nghi ngờ trước những vết thương đến diện kiến Đức Kitô Phục Sinh..."
        )
        player.catalog = [sampleTrack]
        player.currentTrack = sampleTrack
        return player
    }
}
