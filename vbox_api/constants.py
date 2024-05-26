"""
Constants for the VirtualBox API.

Generated from VirtualBox WSDL definitions, with added enumerations for those
not currently specified but used internally, such as MachineFrontend.
"""

from enum import StrEnum


class SettingsVersion(StrEnum):
    """Enumeration for SettingsVersion."""

    NULL = "Null"
    V1_0 = "v1_0"
    V1_1 = "v1_1"
    V1_2 = "v1_2"
    V1_3PRE = "v1_3pre"
    V1_3 = "v1_3"
    V1_4 = "v1_4"
    V1_5 = "v1_5"
    V1_6 = "v1_6"
    V1_7 = "v1_7"
    V1_8 = "v1_8"
    V1_9 = "v1_9"
    V1_10 = "v1_10"
    V1_11 = "v1_11"
    V1_12 = "v1_12"
    V1_13 = "v1_13"
    V1_14 = "v1_14"
    V1_15 = "v1_15"
    V1_16 = "v1_16"
    V1_17 = "v1_17"
    V1_18 = "v1_18"
    V1_19 = "v1_19"
    FUTURE = "Future"


class AccessMode(StrEnum):
    """Enumeration for AccessMode."""

    READ_ONLY = "ReadOnly"
    READ_WRITE = "ReadWrite"


class MachineState(StrEnum):
    """Enumeration for MachineState."""

    NULL = "Null"
    POWERED_OFF = "PoweredOff"
    SAVED = "Saved"
    TELEPORTED = "Teleported"
    ABORTED = "Aborted"
    ABORTED_SAVED = "AbortedSaved"
    RUNNING = "Running"
    PAUSED = "Paused"
    STUCK = "Stuck"
    TELEPORTING = "Teleporting"
    LIVE_SNAPSHOTTING = "LiveSnapshotting"
    STARTING = "Starting"
    STOPPING = "Stopping"
    SAVING = "Saving"
    RESTORING = "Restoring"
    TELEPORTING_PAUSED_VM = "TeleportingPausedVM"
    TELEPORTING_IN = "TeleportingIn"
    DELETING_SNAPSHOT_ONLINE = "DeletingSnapshotOnline"
    DELETING_SNAPSHOT_PAUSED = "DeletingSnapshotPaused"
    ONLINE_SNAPSHOTTING = "OnlineSnapshotting"
    RESTORING_SNAPSHOT = "RestoringSnapshot"
    DELETING_SNAPSHOT = "DeletingSnapshot"
    SETTING_UP = "SettingUp"
    SNAPSHOTTING = "Snapshotting"
    FIRST_ONLINE = "FirstOnline"
    LAST_ONLINE = "LastOnline"
    FIRST_TRANSIENT = "FirstTransient"
    LAST_TRANSIENT = "LastTransient"


class MachineFrontend(StrEnum):
    """Enumeration for MachineFrontend."""

    GUI = "gui"
    HEADLESS = "headless"
    SDL = "sdl"
    EMERGENCY_STOP = "emergencystop"


class SessionState(StrEnum):
    """Enumeration for SessionState."""

    NULL = "Null"
    UNLOCKED = "Unlocked"
    LOCKED = "Locked"
    SPAWNING = "Spawning"
    UNLOCKING = "Unlocking"


class CPUArchitecture(StrEnum):
    """Enumeration for CPUArchitecture."""

    ANY = "Any"
    X86 = "x86"
    AMD64 = "AMD64"


class CPUPropertyType(StrEnum):
    """Enumeration for CPUPropertyType."""

    NULL = "Null"
    PAE = "PAE"
    LONG_MODE = "LongMode"
    TRIPLE_FAULT_RESET = "TripleFaultReset"
    APIC = "APIC"
    X2APIC = "X2APIC"
    IBPB_ON_VM_EXIT = "IBPBOnVMExit"
    IBPB_ON_VM_ENTRY = "IBPBOnVMEntry"
    HW_VIRT = "HWVirt"
    SPEC_CTRL = "SpecCtrl"
    SPEC_CTRL_BY_HOST = "SpecCtrlByHost"
    L1D_FLUSH_ON_EMT_SCHEDULING = "L1DFlushOnEMTScheduling"
    L1D_FLUSH_ON_VM_ENTRY = "L1DFlushOnVMEntry"
    MDS_CLEAR_ON_EMT_SCHEDULING = "MDSClearOnEMTScheduling"
    MDS_CLEAR_ON_VM_ENTRY = "MDSClearOnVMEntry"


class HWVirtExPropertyType(StrEnum):
    """Enumeration for HWVirtExPropertyType."""

    NULL = "Null"
    ENABLED = "Enabled"
    VPID = "VPID"
    NESTED_PAGING = "NestedPaging"
    UNRESTRICTED_EXECUTION = "UnrestrictedExecution"
    LARGE_PAGES = "LargePages"
    FORCE = "Force"
    USE_NATIVE_API = "UseNativeApi"
    VIRT_VMSAVE_VMLOAD = "VirtVmsaveVmload"


class ParavirtProvider(StrEnum):
    """Enumeration for ParavirtProvider."""

    NONE = "None"
    DEFAULT = "Default"
    LEGACY = "Legacy"
    MINIMAL = "Minimal"
    HYPER_V = "HyperV"
    KVM = "KVM"


class LockType(StrEnum):
    """Enumeration for LockType."""

    NULL = "Null"
    SHARED = "Shared"
    WRITE = "Write"
    VM = "VM"


class SessionType(StrEnum):
    """Enumeration for SessionType."""

    NULL = "Null"
    WRITE_LOCK = "WriteLock"
    REMOTE = "Remote"
    SHARED = "Shared"


class DeviceType(StrEnum):
    """Enumeration for DeviceType."""

    NULL = "Null"
    FLOPPY = "Floppy"
    DVD = "DVD"
    HARD_DISK = "HardDisk"
    NETWORK = "Network"
    USB = "USB"
    SHARED_FOLDER = "SharedFolder"
    GRAPHICS_3D = "Graphics3D"
    END = "End"


class DeviceActivity(StrEnum):
    """Enumeration for DeviceActivity."""

    NULL = "Null"
    IDLE = "Idle"
    READING = "Reading"
    WRITING = "Writing"


class ClipboardMode(StrEnum):
    """Enumeration for ClipboardMode."""

    DISABLED = "Disabled"
    HOST_TO_GUEST = "HostToGuest"
    GUEST_TO_HOST = "GuestToHost"
    BIDIRECTIONAL = "Bidirectional"


class DnDMode(StrEnum):
    """Enumeration for DnDMode."""

    DISABLED = "Disabled"
    HOST_TO_GUEST = "HostToGuest"
    GUEST_TO_HOST = "GuestToHost"
    BIDIRECTIONAL = "Bidirectional"


class Scope(StrEnum):
    """Enumeration for Scope."""

    GLOBAL = "Global"
    MACHINE = "Machine"
    SESSION = "Session"


class BIOSBootMenuMode(StrEnum):
    """Enumeration for BIOSBootMenuMode."""

    DISABLED = "Disabled"
    MENU_ONLY = "MenuOnly"
    MESSAGE_AND_MENU = "MessageAndMenu"


class APICMode(StrEnum):
    """Enumeration for APICMode."""

    DISABLED = "Disabled"
    APIC = "APIC"
    X2APIC = "X2APIC"


class ProcessorFeature(StrEnum):
    """Enumeration for ProcessorFeature."""

    HW_VIRT_EX = "HWVirtEx"
    PAE = "PAE"
    LONG_MODE = "LongMode"
    NESTED_PAGING = "NestedPaging"
    UNRESTRICTED_GUEST = "UnrestrictedGuest"
    NESTED_HW_VIRT = "NestedHWVirt"
    VIRT_VMSAVE_VMLOAD = "VirtVmsaveVmload"


class FirmwareType(StrEnum):
    """Enumeration for FirmwareType."""

    BIOS = "BIOS"
    EFI = "EFI"
    EFI32 = "EFI32"
    EFI64 = "EFI64"
    EFIDUAL = "EFIDUAL"


class PointingHIDType(StrEnum):
    """Enumeration for PointingHIDType."""

    NONE = "None"
    PS2_MOUSE = "PS2Mouse"
    USB_MOUSE = "USBMouse"
    USB_TABLET = "USBTablet"
    COMBO_MOUSE = "ComboMouse"
    USB_MULTI_TOUCH = "USBMultiTouch"
    USB_MULTI_TOUCH_SCREEN_PLUS_PAD = "USBMultiTouchScreenPlusPad"


class KeyboardHIDType(StrEnum):
    """Enumeration for KeyboardHIDType."""

    NONE = "None"
    PS2_KEYBOARD = "PS2Keyboard"
    USB_KEYBOARD = "USBKeyboard"
    COMBO_KEYBOARD = "ComboKeyboard"


class BitmapFormat(StrEnum):
    """Enumeration for BitmapFormat."""

    OPAQUE = "Opaque"
    BGR = "BGR"
    BGR0 = "BGR0"
    BGRA = "BGRA"
    RGBA = "RGBA"
    PNG = "PNG"
    JPEG = "JPEG"


class PartitioningType(StrEnum):
    """Enumeration for PartitioningType."""

    MBR = "MBR"
    GPT = "GPT"


class PartitionType(StrEnum):
    """Enumeration for PartitionType."""

    EMPTY = "Empty"
    FAT12 = "FAT12"
    FAT16 = "FAT16"
    FAT = "FAT"
    IFS = "IFS"
    FAT32_CHS = "FAT32CHS"
    FAT32_LBA = "FAT32LBA"
    FAT16_B = "FAT16B"
    EXTENDED = "Extended"
    WINDOWS_RE = "WindowsRE"
    LINUX_SWAP_OLD = "LinuxSwapOld"
    LINUX_OLD = "LinuxOld"
    DRAGONFLY_BSD_SLICE = "DragonFlyBSDSlice"
    LINUX_SWAP = "LinuxSwap"
    LINUX = "Linux"
    LINUX_EXTENDED = "LinuxExtended"
    LINUX_LVM = "LinuxLVM"
    BSD_SLICE = "BSDSlice"
    APPLE_UFS = "AppleUFS"
    APPLE_HFS = "AppleHFS"
    SOLARIS = "Solaris"
    GPT = "GPT"
    EFI = "EFI"
    UNKNOWN = "Unknown"
    MBR = "MBR"
    IFFS = "iFFS"
    SONY_BOOT = "SonyBoot"
    LENOVO_BOOT = "LenovoBoot"
    WINDOWS_MSR = "WindowsMSR"
    WINDOWS_BASIC_DATA = "WindowsBasicData"
    WINDOWS_LDM_META = "WindowsLDMMeta"
    WINDOWS_LDM_DATA = "WindowsLDMData"
    WINDOWS_RECOVERY = "WindowsRecovery"
    WINDOWS_STORAGE_SPACES = "WindowsStorageSpaces"
    WINDOWS_STORAGE_REPLICA = "WindowsStorageReplica"
    IBMGPFS = "IBMGPFS"
    LINUX_DATA = "LinuxData"
    LINUX_RAID = "LinuxRAID"
    LINUX_ROOT_X86 = "LinuxRootX86"
    LINUX_ROOT_AMD64 = "LinuxRootAMD64"
    LINUX_ROOT_ARM32 = "LinuxRootARM32"
    LINUX_ROOT_ARM64 = "LinuxRootARM64"
    LINUX_HOME = "LinuxHome"
    LINUX_SRV = "LinuxSrv"
    LINUX_PLAIN_DM_CRYPT = "LinuxPlainDmCrypt"
    LINUX_LUKS = "LinuxLUKS"
    LINUX_RESERVED = "LinuxReserved"
    FREEBSD_BOOT = "FreeBSDBoot"
    FREEBSD_DATA = "FreeBSDData"
    FREEBSD_SWAP = "FreeBSDSwap"
    FREEBSD_UFS = "FreeBSDUFS"
    FREEBSD_VINUM = "FreeBSDVinum"
    FREEBSD_ZFS = "FreeBSDZFS"
    FREEBSD_UNKNOWN = "FreeBSDUnknown"
    APPLE_HFS_PLUS = "AppleHFSPlus"
    APPLE_APFS = "AppleAPFS"
    APPLE_RAID = "AppleRAID"
    APPLE_RAID_OFFLINE = "AppleRAIDOffline"
    APPLE_BOOT = "AppleBoot"
    APPLE_LABEL = "AppleLabel"
    APPLE_TV_RECOVERY = "AppleTvRecovery"
    APPLE_CORE_STORAGE = "AppleCoreStorage"
    SOFTRAID_STATUS = "SoftRAIDStatus"
    SOFTRAID_SCRATCH = "SoftRAIDScratch"
    SOFTRAID_VOLUME = "SoftRAIDVolume"
    SOFTRAID_CACHE = "SoftRAIDCache"
    APPLE_UNKNOWN = "AppleUnknown"
    SOLARIS_BOOT = "SolarisBoot"
    SOLARIS_ROOT = "SolarisRoot"
    SOLARIS_SWAP = "SolarisSwap"
    SOLARIS_BACKUP = "SolarisBackup"
    SOLARIS_USR = "SolarisUsr"
    SOLARIS_VAR = "SolarisVar"
    SOLARIS_HOME = "SolarisHome"
    SOLARIS_ALT_SECTOR = "SolarisAltSector"
    SOLARIS_RESERVED = "SolarisReserved"
    SOLARIS_UNKNOWN = "SolarisUnknown"
    NETBSD_SWAP = "NetBSDSwap"
    NETBSD_FFS = "NetBSDFFS"
    NETBSD_LFS = "NetBSDLFS"
    NETBSD_RAID = "NetBSDRAID"
    NETBSD_CONCATENATED = "NetBSDConcatenated"
    NETBSD_ENCRYPTED = "NetBSDEncrypted"
    NETBSD_UNKNOWN = "NetBSDUnknown"
    CHROMEOS_KERNEL = "ChromeOSKernel"
    CHROMEOS_ROOT_FS = "ChromeOSRootFS"
    CHROMEOS_FUTURE = "ChromeOSFuture"
    CONTLNX_USR = "ContLnxUsr"
    CONTLNX_ROOT = "ContLnxRoot"
    CONTLNX_RESERVED = "ContLnxReserved"
    CONTLNX_ROOT_RAID = "ContLnxRootRAID"
    HAIKU_BFS = "HaikuBFS"
    MIDNTBSD_BOOT = "MidntBSDBoot"
    MIDNTBSD_DATA = "MidntBSDData"
    MIDNTBSD_SWAP = "MidntBSDSwap"
    MIDNTBSD_UFS = "MidntBSDUFS"
    MIDNTBSD_VIUM = "MidntBSDVium"
    MIDNTBSD_ZFS = "MidntBSDZFS"
    MIDNTBSD_UNKNOWN = "MidntBSDUnknown"
    OPENBSD_DATA = "OpenBSDData"
    QNX_POWER_SAFE_FS = "QNXPowerSafeFS"
    PLAN9 = "Plan9"
    VMWARE_VMK_CORE = "VMWareVMKCore"
    VMWARE_VMFS = "VMWareVMFS"
    VMWARE_RESERVED = "VMWareReserved"
    VMWARE_UNKNOWN = "VMWareUnknown"
    ANDROID_X86_BOOTLOADER = "AndroidX86Bootloader"
    ANDROID_X86_BOOTLOADER2 = "AndroidX86Bootloader2"
    ANDROID_X86_BOOT = "AndroidX86Boot"
    ANDROID_X86_RECOVERY = "AndroidX86Recovery"
    ANDROID_X86_MISC = "AndroidX86Misc"
    ANDROID_X86_METADATA = "AndroidX86Metadata"
    ANDROID_X86_SYSTEM = "AndroidX86System"
    ANDROID_X86_CACHE = "AndroidX86Cache"
    ANDROID_X86_DATA = "AndroidX86Data"
    ANDROID_X86_PERSISTENT = "AndroidX86Persistent"
    ANDROID_X86_VENDOR = "AndroidX86Vendor"
    ANDROID_X86_CONFIG = "AndroidX86Config"
    ANDROID_X86_FACTORY = "AndroidX86Factory"
    ANDROID_X86_FACTORY_ALT = "AndroidX86FactoryAlt"
    ANDROID_X86_FASTBOOT = "AndroidX86Fastboot"
    ANDROID_X86_OEM = "AndroidX86OEM"
    ANDROID_ARM_META = "AndroidARMMeta"
    ANDROID_ARM_EXT = "AndroidARMExt"
    ONIE_BOOT = "ONIEBoot"
    ONIE_CONFIG = "ONIEConfig"
    POWERPC_PREP = "PowerPCPrep"
    XDG_SHR_BOOT_CONFIG = "XDGShrBootConfig"
    CEPH_BLOCK = "CephBlock"
    CEPH_BLOCK_DB = "CephBlockDB"
    CEPH_BLOCK_DB_DMC = "CephBlockDBDmc"
    CEPH_BLOCK_DB_DMC_LUKS = "CephBlockDBDmcLUKS"
    CEPH_BLOCK_DMC = "CephBlockDmc"
    CEPH_BLOCK_DMC_LUKS = "CephBlockDmcLUKS"
    CEPH_BLOCK_WA_LOG = "CephBlockWALog"
    CEPH_BLOCK_WA_LOG_DMC = "CephBlockWALogDmc"
    CEPH_BLOCK_WA_LOG_DMC_LUKS = "CephBlockWALogDmcLUKS"
    CEPH_DISK = "CephDisk"
    CEPH_DISK_DMC = "CephDiskDmc"
    CEPH_JOURNAL = "CephJournal"
    CEPH_JOURNAL_DMC = "CephJournalDmc"
    CEPH_JOURNAL_DMC_LUKS = "CephJournalDmcLUKS"
    CEPH_LOCKBOX = "CephLockbox"
    CEPH_MULTIPATH_BLOCK1 = "CephMultipathBlock1"
    CEPH_MULTIPATH_BLOCK2 = "CephMultipathBlock2"
    CEPH_MULTIPATH_BLOCK_DB = "CephMultipathBlockDB"
    CEPH_MULTIPATH_BLOCK_WA_LOG = "CephMultipathBLockWALog"
    CEPH_MULTIPATH_JOURNAL = "CephMultipathJournal"
    CEPH_MULTIPATH_OSD = "CephMultipathOSD"
    CEPH_OSD = "CephOSD"
    CEPH_OSD_DMC = "CephOSDDmc"
    CEPH_OSD_DMC_LUKS = "CephOSDDmcLUKS"


class DHCPOption(StrEnum):
    """Enumeration for DHCPOption."""

    SUBNET_MASK = "SubnetMask"
    TIME_OFFSET = "TimeOffset"
    ROUTERS = "Routers"
    TIME_SERVERS = "TimeServers"
    NAME_SERVERS = "NameServers"
    DOMAIN_NAME_SERVERS = "DomainNameServers"
    LOG_SERVERS = "LogServers"
    COOKIE_SERVERS = "CookieServers"
    LPR_SERVERS = "LPRServers"
    IMPRESS_SERVERS = "ImpressServers"
    RESOURSE_LOCATION_SERVERS = "ResourseLocationServers"
    HOST_NAME = "HostName"
    BOOT_FILE_SIZE = "BootFileSize"
    MERIT_DUMP_FILE = "MeritDumpFile"
    DOMAIN_NAME = "DomainName"
    SWAP_SERVER = "SwapServer"
    ROOT_PATH = "RootPath"
    EXTENSION_PATH = "ExtensionPath"
    IP_FORWARDING = "IPForwarding"
    OPT_NON_LOCAL_SOURCE_ROUTING = "OptNonLocalSourceRouting"
    POLICY_FILTER = "PolicyFilter"
    MAX_DGRAM_REASSEMBLY_SIZE = "MaxDgramReassemblySize"
    DEFAULT_IPTTL = "DefaultIPTTL"
    PATH_MTU_AGING_TIMEOUT = "PathMTUAgingTimeout"
    PATH_MTU_PLATEAU_TABLE = "PathMTUPlateauTable"
    INTERFACE_MTU = "InterfaceMTU"
    ALL_SUBNETS_ARE_LOCAL = "AllSubnetsAreLocal"
    BROADCAST_ADDRESS = "BroadcastAddress"
    PERFORM_MASK_DISCOVERY = "PerformMaskDiscovery"
    MASK_SUPPLIER = "MaskSupplier"
    PERFORM_ROUTER_DISCOVERY = "PerformRouterDiscovery"
    ROUTER_SOLICITATION_ADDRESS = "RouterSolicitationAddress"
    STATIC_ROUTE = "StaticRoute"
    TRAILER_ENCAPSULATION = "TrailerEncapsulation"
    ARP_CACHE_TIMEOUT = "ARPCacheTimeout"
    ETHERNET_ENCAPSULATION = "EthernetEncapsulation"
    TCP_DEFAULT_TTL = "TCPDefaultTTL"
    TCP_KEEPALIVE_INTERVAL = "TCPKeepaliveInterval"
    TCP_KEEPALIVE_GARBAGE = "TCPKeepaliveGarbage"
    NIS_DOMAIN = "NISDomain"
    NIS_SERVERS = "NISServers"
    NTP_SERVERS = "NTPServers"
    VENDOR_SPECIFIC_INFO = "VendorSpecificInfo"
    NETBIOS_NAME_SERVERS = "NetBIOSNameServers"
    NETBIOS_DATAGRAM_SERVERS = "NetBIOSDatagramServers"
    NETBIOS_NODE_TYPE = "NetBIOSNodeType"
    NETBIOS_SCOPE = "NetBIOSScope"
    X_WINDOWS_FONT_SERVERS = "XWindowsFontServers"
    X_WINDOWS_DISPLAY_MANAGER = "XWindowsDisplayManager"
    NETWARE_IP_DOMAIN_NAME = "NetWareIPDomainName"
    NETWARE_IP_INFORMATION = "NetWareIPInformation"
    NIS_PLUS_DOMAIN = "NISPlusDomain"
    NIS_PLUS_SERVERS = "NISPlusServers"
    TFTP_SERVER_NAME = "TFTPServerName"
    BOOTFILE_NAME = "BootfileName"
    MOBILE_IP_HOME_AGENTS = "MobileIPHomeAgents"
    SMTP_SERVERS = "SMTPServers"
    POP3_SERVERS = "POP3Servers"
    NNTP_SERVERS = "NNTPServers"
    WWW_SERVERS = "WWWServers"
    FINGER_SERVERS = "FingerServers"
    IRC_SERVERS = "IRCServers"
    STREET_TALK_SERVERS = "StreetTalkServers"
    STDA_SERVERS = "STDAServers"
    SLP_DIRECTORY_AGENT = "SLPDirectoryAgent"
    SLP_SERVICE_SCOPE = "SLPServiceScope"
    DOMAIN_SEARCH = "DomainSearch"


class DHCPOptionEncoding(StrEnum):
    """Enumeration for DHCPOptionEncoding."""

    NORMAL = "Normal"
    HEX = "Hex"


class DHCPConfigScope(StrEnum):
    """Enumeration for DHCPConfigScope."""

    GLOBAL = "Global"
    GROUP = "Group"
    MACHINE_NIC = "MachineNIC"
    MAC = "MAC"


class DHCPGroupConditionType(StrEnum):
    """Enumeration for DHCPGroupConditionType."""

    MAC = "MAC"
    MAC_WILDCARD = "MACWildcard"
    VENDOR_CLASS_ID = "vendorClassID"
    VENDOR_CLASS_ID_WILDCARD = "vendorClassIDWildcard"
    USER_CLASS_ID = "userClassID"
    USER_CLASS_ID_WILDCARD = "userClassIDWildcard"


class VFSType(StrEnum):
    """Enumeration for VFSType."""

    FILE = "File"
    CLOUD = "Cloud"
    S3 = "S3"
    WEBDAV = "WebDav"


class ImportOptions(StrEnum):
    """Enumeration for ImportOptions."""

    KEEP_ALL_MACS = "KeepAllMACs"
    KEEP_NAT_MACS = "KeepNATMACs"
    IMPORT_TO_VDI = "ImportToVDI"


class ExportOptions(StrEnum):
    """Enumeration for ExportOptions."""

    CREATE_MANIFEST = "CreateManifest"
    EXPORT_DVD_IMAGES = "ExportDVDImages"
    STRIP_ALL_MACS = "StripAllMACs"
    STRIP_ALL_NON_NAT_MACS = "StripAllNonNATMACs"


class CertificateVersion(StrEnum):
    """Enumeration for CertificateVersion."""

    V1 = "V1"
    V2 = "V2"
    V3 = "V3"
    UNKNOWN = "Unknown"


class VirtualSystemDescriptionType(StrEnum):
    """Enumeration for VirtualSystemDescriptionType."""

    IGNORE = "Ignore"
    OS = "OS"
    NAME = "Name"
    PRODUCT = "Product"
    VENDOR = "Vendor"
    VERSION = "Version"
    PRODUCT_URL = "ProductUrl"
    VENDOR_URL = "VendorUrl"
    DESCRIPTION = "Description"
    LICENSE = "License"
    MISCELLANEOUS = "Miscellaneous"
    CPU = "CPU"
    MEMORY = "Memory"
    HARD_DISK_CONTROLLER_IDE = "HardDiskControllerIDE"
    HARD_DISK_CONTROLLER_SATA = "HardDiskControllerSATA"
    HARD_DISK_CONTROLLER_SCSI = "HardDiskControllerSCSI"
    HARD_DISK_CONTROLLER_SAS = "HardDiskControllerSAS"
    HARD_DISK_IMAGE = "HardDiskImage"
    FLOPPY = "Floppy"
    CDROM = "CDROM"
    NETWORK_ADAPTER = "NetworkAdapter"
    USB_CONTROLLER = "USBController"
    SOUND_CARD = "SoundCard"
    SETTINGS_FILE = "SettingsFile"
    BASE_FOLDER = "BaseFolder"
    PRIMARY_GROUP = "PrimaryGroup"
    CLOUD_INSTANCE_SHAPE = "CloudInstanceShape"
    CLOUD_DOMAIN = "CloudDomain"
    CLOUD_BOOT_DISK_SIZE = "CloudBootDiskSize"
    CLOUD_BUCKET = "CloudBucket"
    CLOUD_OCI_VCN = "CloudOCIVCN"
    CLOUD_PUBLIC_IP = "CloudPublicIP"
    CLOUD_PROFILE_NAME = "CloudProfileName"
    CLOUD_OCI_SUBNET = "CloudOCISubnet"
    CLOUD_KEEP_OBJECT = "CloudKeepObject"
    CLOUD_LAUNCH_INSTANCE = "CloudLaunchInstance"
    CLOUD_INSTANCE_ID = "CloudInstanceId"
    CLOUD_IMAGE_ID = "CloudImageId"
    CLOUD_INSTANCE_STATE = "CloudInstanceState"
    CLOUD_IMAGE_STATE = "CloudImageState"
    CLOUD_INSTANCE_DISPLAY_NAME = "CloudInstanceDisplayName"
    CLOUD_IMAGE_DISPLAY_NAME = "CloudImageDisplayName"
    CLOUD_OCI_LAUNCH_MODE = "CloudOCILaunchMode"
    CLOUD_PRIVATE_IP = "CloudPrivateIP"
    CLOUD_BOOT_VOLUME_ID = "CloudBootVolumeId"
    CLOUD_OCI_VCN_COMPARTMENT = "CloudOCIVCNCompartment"
    CLOUD_OCI_SUBNET_COMPARTMENT = "CloudOCISubnetCompartment"
    CLOUD_PUBLIC_SSH_KEY = "CloudPublicSSHKey"
    BOOTING_FIRMWARE = "BootingFirmware"
    CLOUD_INIT_SCRIPT_PATH = "CloudInitScriptPath"
    CLOUD_COMPARTMENT_ID = "CloudCompartmentId"
    CLOUD_SHAPE_CPUS = "CloudShapeCpus"
    CLOUD_SHAPE_MEMORY = "CloudShapeMemory"
    CLOUD_INSTANCE_METADATA = "CloudInstanceMetadata"
    CLOUD_INSTANCE_FREE_FORM_TAGS = "CloudInstanceFreeFormTags"
    CLOUD_IMAGE_FREE_FORM_TAGS = "CloudImageFreeFormTags"
    HARD_DISK_CONTROLLER_VIRTIO_SCSI = "HardDiskControllerVirtioSCSI"
    HARD_DISK_CONTROLLER_NVME = "HardDiskControllerNVMe"


class VirtualSystemDescriptionValueType(StrEnum):
    """Enumeration for VirtualSystemDescriptionValueType."""

    REFERENCE = "Reference"
    ORIGINAL = "Original"
    AUTO = "Auto"
    EXTRA_CONFIG = "ExtraConfig"


class TpmType(StrEnum):
    """Enumeration for TpmType."""

    NONE = "None"
    V1_2 = "v1_2"
    V2_0 = "v2_0"
    HOST = "Host"
    SWTPM = "Swtpm"


class RecordingDestination(StrEnum):
    """Enumeration for RecordingDestination."""

    NONE = "None"
    FILE = "File"


class RecordingFeature(StrEnum):
    """Enumeration for RecordingFeature."""

    NONE = "None"
    VIDEO = "Video"
    AUDIO = "Audio"


class RecordingAudioCodec(StrEnum):
    """Enumeration for RecordingAudioCodec."""

    NONE = "None"
    WAV_PCM = "WavPCM"
    MP3 = "MP3"
    OGG_VORBIS = "OggVorbis"
    OPUS = "Opus"
    OTHER = "Other"


class RecordingCodecDeadline(StrEnum):
    """Enumeration for RecordingCodecDeadline."""

    DEFAULT = "Default"
    REALTIME = "Realtime"
    GOOD = "Good"
    BEST = "Best"


class RecordingVideoCodec(StrEnum):
    """Enumeration for RecordingVideoCodec."""

    NONE = "None"
    MJPEG = "MJPEG"
    H262 = "H262"
    H264 = "H264"
    H265 = "H265"
    H266 = "H266"
    VP8 = "VP8"
    VP9 = "VP9"
    AV1 = "AV1"
    OTHER = "Other"


class RecordingVideoScalingMode(StrEnum):
    """Enumeration for RecordingVideoScalingMode."""

    NONE = "None"
    NEAREST_NEIGHBOR = "NearestNeighbor"
    BILINEAR = "Bilinear"
    BICUBIC = "Bicubic"


class RecordingRateControlMode(StrEnum):
    """Enumeration for RecordingRateControlMode."""

    ABR = "ABR"
    CBR = "CBR"
    VBR = "VBR"


class SignatureType(StrEnum):
    """Enumeration for SignatureType."""

    X509 = "X509"
    SHA256 = "Sha256"


class UefiVariableAttributes(StrEnum):
    """Enumeration for UefiVariableAttributes."""

    NONE = "None"
    NON_VOLATILE = "NonVolatile"
    BOOT_SERVICE_ACCESS = "BootServiceAccess"
    RUNTIME_ACCESS = "RuntimeAccess"
    HW_ERROR_RECORD = "HwErrorRecord"
    AUTH_WRITE_ACCESS = "AuthWriteAccess"
    AUTH_TIME_BASED_WRITE_ACCESS = "AuthTimeBasedWriteAccess"
    AUTH_APPEND_WRITE = "AuthAppendWrite"


class GraphicsControllerType(StrEnum):
    """Enumeration for GraphicsControllerType."""

    NULL = "Null"
    VBOXVGA = "VBoxVGA"
    VMSVGA = "VMSVGA"
    VBOXSVGA = "VBoxSVGA"


class CleanupMode(StrEnum):
    """Enumeration for CleanupMode."""

    UNREGISTER_ONLY = "UnregisterOnly"
    DETACH_ALL_RETURN_NONE = "DetachAllReturnNone"
    DETACH_ALL_RETURN_HARD_DISKS_ONLY = "DetachAllReturnHardDisksOnly"
    FULL = "Full"
    DETACH_ALL_RETURN_HARD_DISKS_AND_VM_REMOVABLE = (
        "DetachAllReturnHardDisksAndVMRemovable"
    )


class CloneMode(StrEnum):
    """Enumeration for CloneMode."""

    MACHINE_STATE = "MachineState"
    MACHINE_AND_CHILD_STATES = "MachineAndChildStates"
    ALL_STATES = "AllStates"


class CloneOptions(StrEnum):
    """Enumeration for CloneOptions."""

    LINK = "Link"
    KEEP_ALL_MACS = "KeepAllMACs"
    KEEP_NAT_MACS = "KeepNATMACs"
    KEEP_DISK_NAMES = "KeepDiskNames"
    KEEP_HW_UUIDS = "KeepHwUUIDs"


class AutostopType(StrEnum):
    """Enumeration for AutostopType."""

    DISABLED = "Disabled"
    SAVE_STATE = "SaveState"
    POWER_OFF = "PowerOff"
    ACPI_SHUTDOWN = "AcpiShutdown"


class VMProcPriority(StrEnum):
    """Enumeration for VMProcPriority."""

    INVALID = "Invalid"
    DEFAULT = "Default"
    FLAT = "Flat"
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"


class IommuType(StrEnum):
    """Enumeration for IommuType."""

    NONE = "None"
    AUTOMATIC = "Automatic"
    AMD = "AMD"
    INTEL = "Intel"


class HostNetworkInterfaceMediumType(StrEnum):
    """Enumeration for HostNetworkInterfaceMediumType."""

    UNKNOWN = "Unknown"
    ETHERNET = "Ethernet"
    PPP = "PPP"
    SLIP = "SLIP"


class HostNetworkInterfaceStatus(StrEnum):
    """Enumeration for HostNetworkInterfaceStatus."""

    UNKNOWN = "Unknown"
    UP = "Up"
    DOWN = "Down"


class HostNetworkInterfaceType(StrEnum):
    """Enumeration for HostNetworkInterfaceType."""

    BRIDGED = "Bridged"
    HOST_ONLY = "HostOnly"


class UpdateChannel(StrEnum):
    """Enumeration for UpdateChannel."""

    INVALID = "Invalid"
    STABLE = "Stable"
    ALL = "All"
    WITH_BETAS = "WithBetas"
    WITH_TESTING = "WithTesting"


class UpdateSeverity(StrEnum):
    """Enumeration for UpdateSeverity."""

    INVALID = "Invalid"
    CRITICAL = "Critical"
    MAJOR = "Major"
    MINOR = "Minor"
    TESTING = "Testing"


class UpdateState(StrEnum):
    """Enumeration for UpdateState."""

    INVALID = "Invalid"
    AVAILABLE = "Available"
    NOT_AVAILABLE = "NotAvailable"
    DOWNLOADING = "Downloading"
    DOWNLOADED = "Downloaded"
    INSTALLING = "Installing"
    INSTALLED = "Installed"
    USER_INTERACTION = "UserInteraction"
    CANCELED = "Canceled"
    MAINTENANCE = "Maintenance"
    ERROR = "Error"


class ProxyMode(StrEnum):
    """Enumeration for ProxyMode."""

    SYSTEM = "System"
    NO_PROXY = "NoProxy"
    MANUAL = "Manual"


class AdditionsFacilityType(StrEnum):
    """Enumeration for AdditionsFacilityType."""

    NONE = "None"
    VBOX_GUEST_DRIVER = "VBoxGuestDriver"
    AUTO_LOGON = "AutoLogon"
    VBOX_SERVICE = "VBoxService"
    VBOX_TRAY_CLIENT = "VBoxTrayClient"
    SEAMLESS = "Seamless"
    GRAPHICS = "Graphics"
    MONITOR_ATTACH = "MonitorAttach"
    ALL = "All"


class AdditionsFacilityClass(StrEnum):
    """Enumeration for AdditionsFacilityClass."""

    NONE = "None"
    DRIVER = "Driver"
    SERVICE = "Service"
    PROGRAM = "Program"
    FEATURE = "Feature"
    THIRD_PARTY = "ThirdParty"
    ALL = "All"


class AdditionsFacilityStatus(StrEnum):
    """Enumeration for AdditionsFacilityStatus."""

    INACTIVE = "Inactive"
    PAUSED = "Paused"
    PRE_INIT = "PreInit"
    INIT = "Init"
    ACTIVE = "Active"
    TERMINATING = "Terminating"
    TERMINATED = "Terminated"
    FAILED = "Failed"
    UNKNOWN = "Unknown"


class AdditionsRunLevelType(StrEnum):
    """Enumeration for AdditionsRunLevelType."""

    NONE = "None"
    SYSTEM = "System"
    USERLAND = "Userland"
    DESKTOP = "Desktop"


class AdditionsUpdateFlag(StrEnum):
    """Enumeration for AdditionsUpdateFlag."""

    NONE = "None"
    WAIT_FOR_UPDATE_START_ONLY = "WaitForUpdateStartOnly"


class GuestShutdownFlag(StrEnum):
    """Enumeration for GuestShutdownFlag."""

    NONE = "None"
    POWER_OFF = "PowerOff"
    REBOOT = "Reboot"
    FORCE = "Force"


class GuestSessionStatus(StrEnum):
    """Enumeration for GuestSessionStatus."""

    UNDEFINED = "Undefined"
    STARTING = "Starting"
    STARTED = "Started"
    TERMINATING = "Terminating"
    TERMINATED = "Terminated"
    TIMED_OUT_KILLED = "TimedOutKilled"
    TIMED_OUT_ABNORMALLY = "TimedOutAbnormally"
    DOWN = "Down"
    ERROR = "Error"


class GuestSessionWaitForFlag(StrEnum):
    """Enumeration for GuestSessionWaitForFlag."""

    NONE = "None"
    START = "Start"
    TERMINATE = "Terminate"
    STATUS = "Status"


class GuestSessionWaitResult(StrEnum):
    """Enumeration for GuestSessionWaitResult."""

    NONE = "None"
    START = "Start"
    TERMINATE = "Terminate"
    STATUS = "Status"
    ERROR = "Error"
    TIMEOUT = "Timeout"
    WAIT_FLAG_NOT_SUPPORTED = "WaitFlagNotSupported"


class GuestUserState(StrEnum):
    """Enumeration for GuestUserState."""

    UNKNOWN = "Unknown"
    LOGGED_IN = "LoggedIn"
    LOGGED_OUT = "LoggedOut"
    LOCKED = "Locked"
    UNLOCKED = "Unlocked"
    DISABLED = "Disabled"
    IDLE = "Idle"
    IN_USE = "InUse"
    CREATED = "Created"
    DELETED = "Deleted"
    SESSION_CHANGED = "SessionChanged"
    CREDENTIALS_CHANGED = "CredentialsChanged"
    ROLE_CHANGED = "RoleChanged"
    GROUP_ADDED = "GroupAdded"
    GROUP_REMOVED = "GroupRemoved"
    ELEVATED = "Elevated"


class FileSeekOrigin(StrEnum):
    """Enumeration for FileSeekOrigin."""

    BEGIN = "Begin"
    CURRENT = "Current"
    END = "End"


class ProcessInputFlag(StrEnum):
    """Enumeration for ProcessInputFlag."""

    NONE = "None"
    END_OF_FILE = "EndOfFile"


class ProcessOutputFlag(StrEnum):
    """Enumeration for ProcessOutputFlag."""

    NONE = "None"
    STD_ERR = "StdErr"


class ProcessWaitForFlag(StrEnum):
    """Enumeration for ProcessWaitForFlag."""

    NONE = "None"
    START = "Start"
    TERMINATE = "Terminate"
    STD_IN = "StdIn"
    STD_OUT = "StdOut"
    STD_ERR = "StdErr"


class ProcessWaitResult(StrEnum):
    """Enumeration for ProcessWaitResult."""

    NONE = "None"
    START = "Start"
    TERMINATE = "Terminate"
    STATUS = "Status"
    ERROR = "Error"
    TIMEOUT = "Timeout"
    STD_IN = "StdIn"
    STD_OUT = "StdOut"
    STD_ERR = "StdErr"
    WAIT_FLAG_NOT_SUPPORTED = "WaitFlagNotSupported"


class FileCopyFlag(StrEnum):
    """Enumeration for FileCopyFlag."""

    NONE = "None"
    NO_REPLACE = "NoReplace"
    FOLLOW_LINKS = "FollowLinks"
    UPDATE = "Update"


class FsObjMoveFlag(StrEnum):
    """Enumeration for FsObjMoveFlag."""

    NONE = "None"
    REPLACE = "Replace"
    FOLLOW_LINKS = "FollowLinks"
    ALLOW_DIRECTORY_MOVES = "AllowDirectoryMoves"


class DirectoryCreateFlag(StrEnum):
    """Enumeration for DirectoryCreateFlag."""

    NONE = "None"
    PARENTS = "Parents"


class DirectoryCopyFlag(StrEnum):
    """Enumeration for DirectoryCopyFlag."""

    NONE = "None"
    COPY_INTO_EXISTING = "CopyIntoExisting"
    RECURSIVE = "Recursive"
    FOLLOW_LINKS = "FollowLinks"


class DirectoryRemoveRecFlag(StrEnum):
    """Enumeration for DirectoryRemoveRecFlag."""

    NONE = "None"
    CONTENT_AND_DIR = "ContentAndDir"
    CONTENT_ONLY = "ContentOnly"


class FsObjRenameFlag(StrEnum):
    """Enumeration for FsObjRenameFlag."""

    NO_REPLACE = "NoReplace"
    REPLACE = "Replace"


class ProcessCreateFlag(StrEnum):
    """Enumeration for ProcessCreateFlag."""

    NONE = "None"
    WAIT_FOR_PROCESS_START_ONLY = "WaitForProcessStartOnly"
    IGNORE_ORPHANED_PROCESSES = "IgnoreOrphanedProcesses"
    HIDDEN = "Hidden"
    PROFILE = "Profile"
    WAIT_FOR_STD_OUT = "WaitForStdOut"
    WAIT_FOR_STD_ERR = "WaitForStdErr"
    EXPAND_ARGUMENTS = "ExpandArguments"
    UNQUOTED_ARGUMENTS = "UnquotedArguments"


class ProcessPriority(StrEnum):
    """Enumeration for ProcessPriority."""

    INVALID = "Invalid"
    DEFAULT = "Default"


class SymlinkType(StrEnum):
    """Enumeration for SymlinkType."""

    UNKNOWN = "Unknown"
    DIRECTORY = "Directory"
    FILE = "File"


class SymlinkReadFlag(StrEnum):
    """Enumeration for SymlinkReadFlag."""

    NONE = "None"
    NO_SYMLINKS = "NoSymlinks"


class ProcessStatus(StrEnum):
    """Enumeration for ProcessStatus."""

    UNDEFINED = "Undefined"
    STARTING = "Starting"
    STARTED = "Started"
    PAUSED = "Paused"
    TERMINATING = "Terminating"
    TERMINATED_NORMALLY = "TerminatedNormally"
    TERMINATED_SIGNAL = "TerminatedSignal"
    TERMINATED_ABNORMALLY = "TerminatedAbnormally"
    TIMED_OUT_KILLED = "TimedOutKilled"
    TIMED_OUT_ABNORMALLY = "TimedOutAbnormally"
    DOWN = "Down"
    ERROR = "Error"


class ProcessInputStatus(StrEnum):
    """Enumeration for ProcessInputStatus."""

    UNDEFINED = "Undefined"
    BROKEN = "Broken"
    AVAILABLE = "Available"
    WRITTEN = "Written"
    OVERFLOW = "Overflow"


class PathStyle(StrEnum):
    """Enumeration for PathStyle."""

    DOS = "DOS"
    UNIX = "UNIX"
    UNKNOWN = "Unknown"


class FileAccessMode(StrEnum):
    """Enumeration for FileAccessMode."""

    READ_ONLY = "ReadOnly"
    WRITE_ONLY = "WriteOnly"
    READ_WRITE = "ReadWrite"
    APPEND_ONLY = "AppendOnly"
    APPEND_READ = "AppendRead"


class FileOpenAction(StrEnum):
    """Enumeration for FileOpenAction."""

    OPEN_EXISTING = "OpenExisting"
    OPEN_OR_CREATE = "OpenOrCreate"
    CREATE_NEW = "CreateNew"
    CREATE_OR_REPLACE = "CreateOrReplace"
    OPEN_EXISTING_TRUNCATED = "OpenExistingTruncated"
    APPEND_OR_CREATE = "AppendOrCreate"


class FileSharingMode(StrEnum):
    """Enumeration for FileSharingMode."""

    READ = "Read"
    WRITE = "Write"
    READ_WRITE = "ReadWrite"
    DELETE = "Delete"
    READ_DELETE = "ReadDelete"
    WRITE_DELETE = "WriteDelete"
    ALL = "All"


class FileOpenExFlag(StrEnum):
    """Enumeration for FileOpenExFlag."""

    NONE = "None"


class FileStatus(StrEnum):
    """Enumeration for FileStatus."""

    UNDEFINED = "Undefined"
    OPENING = "Opening"
    OPEN = "Open"
    CLOSING = "Closing"
    CLOSED = "Closed"
    DOWN = "Down"
    ERROR = "Error"


class FsObjType(StrEnum):
    """Enumeration for FsObjType."""

    UNKNOWN = "Unknown"
    FIFO = "Fifo"
    DEV_CHAR = "DevChar"
    DIRECTORY = "Directory"
    DEV_BLOCK = "DevBlock"
    FILE = "File"
    SYMLINK = "Symlink"
    SOCKET = "Socket"
    WHITE_OUT = "WhiteOut"


class DnDAction(StrEnum):
    """Enumeration for DnDAction."""

    IGNORE = "Ignore"
    COPY = "Copy"
    MOVE = "Move"
    LINK = "Link"


class DirectoryOpenFlag(StrEnum):
    """Enumeration for DirectoryOpenFlag."""

    NONE = "None"
    NO_SYMLINKS = "NoSymlinks"


class MediumState(StrEnum):
    """Enumeration for MediumState."""

    NOT_CREATED = "NotCreated"
    CREATED = "Created"
    LOCKED_READ = "LockedRead"
    LOCKED_WRITE = "LockedWrite"
    INACCESSIBLE = "Inaccessible"
    CREATING = "Creating"
    DELETING = "Deleting"


class MediumType(StrEnum):
    """Enumeration for MediumType."""

    NORMAL = "Normal"
    IMMUTABLE = "Immutable"
    WRITETHROUGH = "Writethrough"
    SHAREABLE = "Shareable"
    READONLY = "Readonly"
    MULTI_ATTACH = "MultiAttach"


class MediumDeviceType(StrEnum):
    """Enumeration for MediumDeviceType."""

    FLOPPY = "Floppy"
    DVD = "DVD"
    HARD_DISK = "HardDisk"


class MediumVariant(StrEnum):
    """Enumeration for MediumVariant."""

    STANDARD = "Standard"
    VMDK_SPLIT_2G = "VmdkSplit2G"
    VMDK_RAW_DISK = "VmdkRawDisk"
    VMDK_STREAM_OPTIMIZED = "VmdkStreamOptimized"
    VMDK_ESX = "VmdkESX"
    VDI_ZERO_EXPAND = "VdiZeroExpand"
    FIXED = "Fixed"
    DIFF = "Diff"
    FORMATTED = "Formatted"
    NO_CREATE_DIR = "NoCreateDir"


class DataType(StrEnum):
    """Enumeration for DataType."""

    INT32 = "Int32"
    INT8 = "Int8"
    STRING = "String"


class DataFlags(StrEnum):
    """Enumeration for DataFlags."""

    NONE = "None"
    MANDATORY = "Mandatory"
    EXPERT = "Expert"
    ARRAY = "Array"
    FLAG_MASK = "FlagMask"


class MediumFormatCapabilities(StrEnum):
    """Enumeration for MediumFormatCapabilities."""

    UUID = "Uuid"
    CREATE_FIXED = "CreateFixed"
    CREATE_DYNAMIC = "CreateDynamic"
    CREATE_SPLIT_2G = "CreateSplit2G"
    DIFFERENCING = "Differencing"
    ASYNCHRONOUS = "Asynchronous"
    FILE = "File"
    PROPERTIES = "Properties"
    TCP_NETWORKING = "TcpNetworking"
    VFS = "VFS"
    DISCARD = "Discard"
    PREFERRED = "Preferred"
    CAPABILITY_MASK = "CapabilityMask"


class PartitionTableType(StrEnum):
    """Enumeration for PartitionTableType."""

    MBR = "MBR"
    GPT = "GPT"


class KeyboardLED(StrEnum):
    """Enumeration for KeyboardLED."""

    NUM_LOCK = "NumLock"
    CAPS_LOCK = "CapsLock"
    SCROLL_LOCK = "ScrollLock"


class MouseButtonState(StrEnum):
    """Enumeration for MouseButtonState."""

    LEFT_BUTTON = "LeftButton"
    RIGHT_BUTTON = "RightButton"
    MIDDLE_BUTTON = "MiddleButton"
    WHEEL_UP = "WheelUp"
    WHEEL_DOWN = "WheelDown"
    X_BUTTON1 = "XButton1"
    X_BUTTON2 = "XButton2"
    MOUSE_STATE_MASK = "MouseStateMask"


class TouchContactState(StrEnum):
    """Enumeration for TouchContactState."""

    NONE = "None"
    IN_CONTACT = "InContact"
    IN_RANGE = "InRange"
    CONTACT_STATE_MASK = "ContactStateMask"


class FramebufferCapabilities(StrEnum):
    """Enumeration for FramebufferCapabilities."""

    UPDATE_IMAGE = "UpdateImage"
    VHWA = "VHWA"
    VISIBLE_REGION = "VisibleRegion"
    RENDER_CURSOR = "RenderCursor"
    MOVE_CURSOR = "MoveCursor"


class GuestMonitorStatus(StrEnum):
    """Enumeration for GuestMonitorStatus."""

    DISABLED = "Disabled"
    ENABLED = "Enabled"
    BLANK = "Blank"


class ScreenLayoutMode(StrEnum):
    """Enumeration for ScreenLayoutMode."""

    APPLY = "Apply"
    RESET = "Reset"
    ATTACH = "Attach"
    SILENT = "Silent"


class NetworkAttachmentType(StrEnum):
    """Enumeration for NetworkAttachmentType."""

    NULL = "Null"
    NAT = "NAT"
    BRIDGED = "Bridged"
    INTERNAL = "Internal"
    HOST_ONLY = "HostOnly"
    GENERIC = "Generic"
    NAT_NETWORK = "NATNetwork"
    CLOUD = "Cloud"
    HOST_ONLY_NETWORK = "HostOnlyNetwork"


class NetworkAdapterType(StrEnum):
    """Enumeration for NetworkAdapterType."""

    NULL = "Null"
    AM79C970A = "Am79C970A"
    AM79C973 = "Am79C973"
    I82540EM = "I82540EM"
    I82543GC = "I82543GC"
    I82545EM = "I82545EM"
    VIRTIO = "Virtio"
    AM79C960 = "Am79C960"
    NE2000 = "NE2000"
    NE1000 = "NE1000"
    WD8013 = "WD8013"
    WD8003 = "WD8003"
    ELNK2 = "ELNK2"
    ELNK1 = "ELNK1"


class NetworkAdapterPromiscModePolicy(StrEnum):
    """Enumeration for NetworkAdapterPromiscModePolicy."""

    DENY = "Deny"
    ALLOW_NETWORK = "AllowNetwork"
    ALLOW_ALL = "AllowAll"


class PortMode(StrEnum):
    """Enumeration for PortMode."""

    DISCONNECTED = "Disconnected"
    HOST_PIPE = "HostPipe"
    HOST_DEVICE = "HostDevice"
    RAW_FILE = "RawFile"
    TCP = "TCP"


class UartType(StrEnum):
    """Enumeration for UartType."""

    U16450 = "U16450"
    U16550A = "U16550A"
    U16750 = "U16750"


class VMExecutionEngine(StrEnum):
    """Enumeration for VMExecutionEngine."""

    NOT_SET = "NotSet"
    EMULATED = "Emulated"
    HW_VIRT = "HwVirt"
    NATIVE_API = "NativeApi"


class USBControllerType(StrEnum):
    """Enumeration for USBControllerType."""

    NULL = "Null"
    OHCI = "OHCI"
    EHCI = "EHCI"
    XHCI = "XHCI"
    LAST = "Last"


class USBConnectionSpeed(StrEnum):
    """Enumeration for USBConnectionSpeed."""

    NULL = "Null"
    LOW = "Low"
    FULL = "Full"
    HIGH = "High"
    SUPER = "Super"
    SUPER_PLUS = "SuperPlus"


class USBDeviceState(StrEnum):
    """Enumeration for USBDeviceState."""

    NOT_SUPPORTED = "NotSupported"
    UNAVAILABLE = "Unavailable"
    BUSY = "Busy"
    AVAILABLE = "Available"
    HELD = "Held"
    CAPTURED = "Captured"


class USBDeviceFilterAction(StrEnum):
    """Enumeration for USBDeviceFilterAction."""

    NULL = "Null"
    IGNORE = "Ignore"
    HOLD = "Hold"


class AudioDriverType(StrEnum):
    """Enumeration for AudioDriverType."""

    DEFAULT = "Default"
    NULL = "Null"
    OSS = "OSS"
    ALSA = "ALSA"
    PULSE = "Pulse"
    WIN_MM = "WinMM"
    DIRECT_SOUND = "DirectSound"
    WAS = "WAS"
    CORE_AUDIO = "CoreAudio"
    MMPM = "MMPM"
    SOL_AUDIO = "SolAudio"


class AudioControllerType(StrEnum):
    """Enumeration for AudioControllerType."""

    AC97 = "AC97"
    SB16 = "SB16"
    HDA = "HDA"


class AudioCodecType(StrEnum):
    """Enumeration for AudioCodecType."""

    NULL = "Null"
    SB16 = "SB16"
    STAC9700 = "STAC9700"
    AD1980 = "AD1980"
    STAC9221 = "STAC9221"


class AudioDirection(StrEnum):
    """Enumeration for AudioDirection."""

    UNKNOWN = "Unknown"
    IN = "In"
    OUT = "Out"
    DUPLEX = "Duplex"


class AudioDeviceType(StrEnum):
    """Enumeration for AudioDeviceType."""

    UNKNOWN = "Unknown"
    BUILT_LIN = "BuiltLin"
    EXTERNAL_USB = "ExternalUSB"
    EXTERNAL_OTHER = "ExternalOther"


class AudioDeviceState(StrEnum):
    """Enumeration for AudioDeviceState."""

    UNKNOWN = "Unknown"
    ACTIVE = "Active"
    DISABLED = "Disabled"
    NOT_PRESENT = "NotPresent"
    UNPLUGGED = "Unplugged"


class AuthType(StrEnum):
    """Enumeration for AuthType."""

    NULL = "Null"
    EXTERNAL = "External"
    GUEST = "Guest"


class Reason(StrEnum):
    """Enumeration for Reason."""

    UNSPECIFIED = "Unspecified"
    HOST_SUSPEND = "HostSuspend"
    HOST_RESUME = "HostResume"
    HOST_BATTERY_LOW = "HostBatteryLow"
    SNAPSHOT = "Snapshot"


class StorageBus(StrEnum):
    """Enumeration for StorageBus."""

    NULL = "Null"
    IDE = "IDE"
    SATA = "SATA"
    SCSI = "SCSI"
    FLOPPY = "Floppy"
    SAS = "SAS"
    USB = "USB"
    PCIE = "PCIe"
    VIRTIO_SCSI = "VirtioSCSI"


class StorageControllerType(StrEnum):
    """Enumeration for StorageControllerType."""

    NULL = "Null"
    LSILOGIC = "LsiLogic"
    BUSLOGIC = "BusLogic"
    INTEL_AHCI = "IntelAhci"
    PIIX3 = "PIIX3"
    PIIX4 = "PIIX4"
    ICH6 = "ICH6"
    I82078 = "I82078"
    LSILOGIC_SAS = "LsiLogicSas"
    USB = "USB"
    NVME = "NVMe"
    VIRTIO_SCSI = "VirtioSCSI"


class ChipsetType(StrEnum):
    """Enumeration for ChipsetType."""

    NULL = "Null"
    PIIX3 = "PIIX3"
    ICH9 = "ICH9"


class NATAliasMode(StrEnum):
    """Enumeration for NATAliasMode."""

    ALIAS_LOG = "AliasLog"
    ALIAS_PROXY_ONLY = "AliasProxyOnly"
    ALIAS_USE_SAME_PORTS = "AliasUseSamePorts"


class NATProtocol(StrEnum):
    """Enumeration for NATProtocol."""

    UDP = "UDP"
    TCP = "TCP"


class BandwidthGroupType(StrEnum):
    """Enumeration for BandwidthGroupType."""

    NULL = "Null"
    DISK = "Disk"
    NETWORK = "Network"


class GuestDebugProvider(StrEnum):
    """Enumeration for GuestDebugProvider."""

    NONE = "None"
    NATIVE = "Native"
    GDB = "GDB"
    KD = "KD"


class GuestDebugIoProvider(StrEnum):
    """Enumeration for GuestDebugIoProvider."""

    NONE = "None"
    TCP = "TCP"
    UDP = "UDP"
    IPC = "IPC"


class VBoxEventType(StrEnum):
    """Enumeration for VBoxEventType."""

    INVALID = "Invalid"
    ANY = "Any"
    VETOABLE = "Vetoable"
    MACHINE_EVENT = "MachineEvent"
    SNAPSHOT_EVENT = "SnapshotEvent"
    INPUT_EVENT = "InputEvent"
    LAST_WILDCARD = "LastWildcard"
    ON_MACHINE_STATE_CHANGED = "OnMachineStateChanged"
    ON_MACHINE_DATA_CHANGED = "OnMachineDataChanged"
    ON_EXTRA_DATA_CHANGED = "OnExtraDataChanged"
    ON_EXTRA_DATA_CAN_CHANGE = "OnExtraDataCanChange"
    ON_MEDIUM_REGISTERED = "OnMediumRegistered"
    ON_MACHINE_REGISTERED = "OnMachineRegistered"
    ON_SESSION_STATE_CHANGED = "OnSessionStateChanged"
    ON_SNAPSHOT_TAKEN = "OnSnapshotTaken"
    ON_SNAPSHOT_DELETED = "OnSnapshotDeleted"
    ON_SNAPSHOT_CHANGED = "OnSnapshotChanged"
    ON_GUEST_PROPERTY_CHANGED = "OnGuestPropertyChanged"
    ON_MOUSE_POINTER_SHAPE_CHANGED = "OnMousePointerShapeChanged"
    ON_MOUSE_CAPABILITY_CHANGED = "OnMouseCapabilityChanged"
    ON_KEYBOARD_LEDS_CHANGED = "OnKeyboardLedsChanged"
    ON_STATE_CHANGED = "OnStateChanged"
    ON_ADDITIONS_STATE_CHANGED = "OnAdditionsStateChanged"
    ON_NETWORK_ADAPTER_CHANGED = "OnNetworkAdapterChanged"
    ON_SERIAL_PORT_CHANGED = "OnSerialPortChanged"
    ON_PARALLEL_PORT_CHANGED = "OnParallelPortChanged"
    ON_STORAGE_CONTROLLER_CHANGED = "OnStorageControllerChanged"
    ON_MEDIUM_CHANGED = "OnMediumChanged"
    ON_VRDE_SERVER_CHANGED = "OnVRDEServerChanged"
    ON_USB_CONTROLLER_CHANGED = "OnUSBControllerChanged"
    ON_USB_DEVICE_STATE_CHANGED = "OnUSBDeviceStateChanged"
    ON_SHARED_FOLDER_CHANGED = "OnSharedFolderChanged"
    ON_RUNTIME_ERROR = "OnRuntimeError"
    ON_CAN_SHOW_WINDOW = "OnCanShowWindow"
    ON_SHOW_WINDOW = "OnShowWindow"
    ON_CPU_CHANGED = "OnCPUChanged"
    ON_VRDE_SERVER_INFO_CHANGED = "OnVRDEServerInfoChanged"
    ON_EVENT_SOURCE_CHANGED = "OnEventSourceChanged"
    ON_CPU_EXECUTION_CAP_CHANGED = "OnCPUExecutionCapChanged"
    ON_GUEST_KEYBOARD = "OnGuestKeyboard"
    ON_GUEST_MOUSE = "OnGuestMouse"
    ON_NAT_REDIRECT = "OnNATRedirect"
    ON_HOST_PCI_DEVICE_PLUG = "OnHostPCIDevicePlug"
    ON_VBOX_SVC_AVAILABILITY_CHANGED = "OnVBoxSVCAvailabilityChanged"
    ON_BANDWIDTH_GROUP_CHANGED = "OnBandwidthGroupChanged"
    ON_GUEST_MONITOR_CHANGED = "OnGuestMonitorChanged"
    ON_STORAGE_DEVICE_CHANGED = "OnStorageDeviceChanged"
    ON_CLIPBOARD_MODE_CHANGED = "OnClipboardModeChanged"
    ON_DND_MODE_CHANGED = "OnDnDModeChanged"
    ON_NAT_NETWORK_CHANGED = "OnNATNetworkChanged"
    ON_NAT_NETWORK_START_STOP = "OnNATNetworkStartStop"
    ON_NAT_NETWORK_ALTER = "OnNATNetworkAlter"
    ON_NAT_NETWORK_CREATION_DELETION = "OnNATNetworkCreationDeletion"
    ON_NAT_NETWORK_SETTING = "OnNATNetworkSetting"
    ON_NAT_NETWORK_PORT_FORWARD = "OnNATNetworkPortForward"
    ON_GUEST_SESSION_STATE_CHANGED = "OnGuestSessionStateChanged"
    ON_GUEST_SESSION_REGISTERED = "OnGuestSessionRegistered"
    ON_GUEST_PROCESS_REGISTERED = "OnGuestProcessRegistered"
    ON_GUEST_PROCESS_STATE_CHANGED = "OnGuestProcessStateChanged"
    ON_GUEST_PROCESS_INPUT_NOTIFY = "OnGuestProcessInputNotify"
    ON_GUEST_PROCESS_OUTPUT = "OnGuestProcessOutput"
    ON_GUEST_FILE_REGISTERED = "OnGuestFileRegistered"
    ON_GUEST_FILE_STATE_CHANGED = "OnGuestFileStateChanged"
    ON_GUEST_FILE_OFFSET_CHANGED = "OnGuestFileOffsetChanged"
    ON_GUEST_FILE_READ = "OnGuestFileRead"
    ON_GUEST_FILE_WRITE = "OnGuestFileWrite"
    ON_RECORDING_CHANGED = "OnRecordingChanged"
    ON_GUEST_USER_STATE_CHANGED = "OnGuestUserStateChanged"
    ON_GUEST_MULTI_TOUCH = "OnGuestMultiTouch"
    ON_HOST_NAME_RESOLUTION_CONFIGURATION_CHANGE = (
        "OnHostNameResolutionConfigurationChange"
    )
    ON_SNAPSHOT_RESTORED = "OnSnapshotRestored"
    ON_MEDIUM_CONFIG_CHANGED = "OnMediumConfigChanged"
    ON_AUDIO_ADAPTER_CHANGED = "OnAudioAdapterChanged"
    ON_PROGRESS_PERCENTAGE_CHANGED = "OnProgressPercentageChanged"
    ON_PROGRESS_TASK_COMPLETED = "OnProgressTaskCompleted"
    ON_CURSOR_POSITION_CHANGED = "OnCursorPositionChanged"
    ON_GUEST_ADDITIONS_STATUS_CHANGED = "OnGuestAdditionsStatusChanged"
    ON_GUEST_MONITOR_INFO_CHANGED = "OnGuestMonitorInfoChanged"
    ON_GUEST_FILE_SIZE_CHANGED = "OnGuestFileSizeChanged"
    ON_CLIPBOARD_FILE_TRANSFER_MODE_CHANGED = "OnClipboardFileTransferModeChanged"
    ON_CLOUD_PROVIDER_LIST_CHANGED = "OnCloudProviderListChanged"
    ON_CLOUD_PROVIDER_REGISTERED = "OnCloudProviderRegistered"
    ON_CLOUD_PROVIDER_UNINSTALL = "OnCloudProviderUninstall"
    ON_CLOUD_PROFILE_REGISTERED = "OnCloudProfileRegistered"
    ON_CLOUD_PROFILE_CHANGED = "OnCloudProfileChanged"
    ON_PROGRESS_CREATED = "OnProgressCreated"
    ON_LANGUAGE_CHANGED = "OnLanguageChanged"
    ON_UPDATE_AGENT_AVAILABLE = "OnUpdateAgentAvailable"
    ON_UPDATE_AGENT_ERROR = "OnUpdateAgentError"
    ON_UPDATE_AGENT_SETTINGS_CHANGED = "OnUpdateAgentSettingsChanged"
    ON_UPDATE_AGENT_STATE_CHANGED = "OnUpdateAgentStateChanged"
    ON_HOST_AUDIO_DEVICE_CHANGED = "OnHostAudioDeviceChanged"
    ON_GUEST_DEBUG_CONTROL_CHANGED = "OnGuestDebugControlChanged"
    ON_MACHINE_GROUPS_CHANGED = "OnMachineGroupsChanged"
    END = "End"


class GuestMouseEventMode(StrEnum):
    """Enumeration for GuestMouseEventMode."""

    RELATIVE = "Relative"
    ABSOLUTE = "Absolute"


class GuestMonitorChangedEventType(StrEnum):
    """Enumeration for GuestMonitorChangedEventType."""

    ENABLED = "Enabled"
    DISABLED = "Disabled"
    NEW_ORIGIN = "NewOrigin"


class FormValueType(StrEnum):
    """Enumeration for FormValueType."""

    BOOLEAN = "Boolean"
    STRING = "String"
    CHOICE = "Choice"
    RANGED_INTEGER = "RangedInteger"
    RANGED_INTEGER64 = "RangedInteger64"


class CloudMachineState(StrEnum):
    """Enumeration for CloudMachineState."""

    INVALID = "Invalid"
    PROVISIONING = "Provisioning"
    RUNNING = "Running"
    STARTING = "Starting"
    STOPPING = "Stopping"
    STOPPED = "Stopped"
    CREATING_IMAGE = "CreatingImage"
    TERMINATING = "Terminating"
    TERMINATED = "Terminated"


class CloudImageState(StrEnum):
    """Enumeration for CloudImageState."""

    INVALID = "Invalid"
    PROVISIONING = "Provisioning"
    IMPORTING = "Importing"
    AVAILABLE = "Available"
    EXPORTING = "Exporting"
    DISABLED = "Disabled"
    DELETED = "Deleted"


class VrdeExtPack(StrEnum):
    """Enumeration for VrdeExtPack."""

    ORACLE_VM_VIRTUALBOX_EXTENSION_PACK = "Oracle VM VirtualBox Extension Pack"
    VNC = "VNC"
