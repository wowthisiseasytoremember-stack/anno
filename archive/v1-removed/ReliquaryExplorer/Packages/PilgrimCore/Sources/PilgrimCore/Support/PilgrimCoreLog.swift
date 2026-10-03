import Foundation
import OSLog

/// Central logging identities so every subsystem is greppable in
/// Console / sysdiagnose.
public enum PilgrimCoreLog {
    public static let subsystem = "org.pilgrimage.ReliquaryExplorer"

    public static let ar = Logger(subsystem: subsystem, category: "AR")
    public static let geofence = Logger(subsystem: subsystem, category: "Geofence")
    public static let audio = Logger(subsystem: subsystem, category: "Hagiography")
    public static let coordinator = Logger(subsystem: subsystem, category: "PilgrimGuide")
}
