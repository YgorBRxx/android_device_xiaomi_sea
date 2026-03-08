#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.tools import (
    llvm_objdump_path,
)
from extract_utils.utils import (
    run_cmd,
)

namespace_imports = [
	'device/xiaomi/sea',
	'hardware/mediatek',
	'hardware/xiaomi',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups
}

blob_fixups: blob_fixups_user_type = {
    ('vendor/lib64/libaalservice.so', 'vendor/lib64/libcam.utils.sensorprovider.so'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V1-ndk.so')
        .replace_needed('android.hardware.sensors-V1-ndk.so', 'android.hardware.sensors-V3-ndk.so'),

    ('vendor/bin/hw/android.hardware.health-service.example'): blob_fixup()
        .replace_needed('android.hardware.health-V3-ndk.so', 'android.hardware.health-V4-ndk.so'),

    ('vendor/lib/libaalservice.so'): blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),

    ('vendor/lib/libsensorndkbridge.so', 'vendor/lib64/libsensorndkbridge.so', 'vendor/bin/hw/android.hardware.sensors-service.multihal'): blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),

    ('vendor/bin/mnld'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),

    (
        'vendor/lib/egl/libGLES_mali.so',
        'vendor/lib64/egl/libGLES_mali.so',
        'vendor/lib/hw/android.hardware.graphics.allocator-V2-mediatek.so',
        'vendor/lib64/hw/android.hardware.graphics.allocator-V2-mediatek.so',
        'vendor/lib/hw/mapper.mediatek.so',
        'vendor/lib64/hw/mapper.mediatek.so',
        'vendor/lib/libcodec2_fsr.so',
        'vendor/lib64/libcodec2_fsr.so',
        'vendor/lib/libgpud.so',
        'vendor/lib64/libgpud.so',
        'vendor/lib/libmtkcam_grallocutils.so',
        'vendor/lib64/libmtkcam_grallocutils.so',
        'vendor/lib/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
        'vendor/lib/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
        'vendor/lib/vendor.mediatek.hardware.pq_aidl-V7-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so',
        'vendor/lib64/libaimemc.so',
        'vendor/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so',
        'vendor/bin/hw/android.hardware.graphics.allocator-V2-service-mediatek'
    ): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V6-ndk.so'),

    (
        'vendor/lib/android.hardware.audio.core-impl-mediatek.so',
        'vendor/lib64/android.hardware.audio.core-impl-mediatek.so',
        'vendor/lib/hw/android.hardware.soundtrigger3-impl.so',
        'vendor/lib64/hw/android.hardware.soundtrigger3-impl.so',
        'vendor/lib/soundfx/libmisoundfx_aidl.so',
        'vendor/lib64/soundfx/libmisoundfx_aidl.so',
        'vendor/bin/hw/android.hardware.audio.service-aidl.mediatek'
    ): blob_fixup()
        .remove_needed('libaudio_aidl_conversion_common_ndk.so'),

    ('vendor/lib/vendor.mediatek.hardware.pq_aidl-V7-ndk.so', 'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V6-ndk.so'),

    ('vendor/lib/hw/audio.bluetooth.default.so', 'vendor/lib64/hw/audio.bluetooth.default.so'): blob_fixup()
        .remove_needed('libbluetooth_audio_session_aidl_mtk.so')
        .replace_needed('android.hardware.bluetooth.audio-V4-ndk.so', 'android.hardware.bluetooth.audio-V5-ndk.so')
        .replace_needed('android.hardware.audio.common-V3-ndk.so', 'android.hardware.audio.common-V4-ndk.so'),

    ('vendor/lib/libbluetooth_audio_session_aidl.so', 'vendor/lib64/libbluetooth_audio_session_aidl.so'): blob_fixup()
        .replace_needed('android.hardware.bluetooth.audio-V4-ndk.so', 'android.hardware.bluetooth.audio-V5-ndk.so'),

    (
        'vendor/lib/soundfx/libbundleaidl.so', 'vendor/lib64/soundfx/libbundleaidl.so',
        'vendor/lib/soundfx/libextensioneffect.so', 'vendor/lib64/soundfx/libextensioneffect.so',
        'vendor/lib/soundfx/libpreprocessingaidl.so', 'vendor/lib64/soundfx/libpreprocessingaidl.so',
        'vendor/lib/soundfx/libvolumesw.so', 'vendor/lib64/soundfx/libvolumesw.so',
        'vendor/lib/soundfx/libagc1sw.so', 'vendor/lib64/soundfx/libagc1sw.so',
        'vendor/lib/soundfx/libpresetreverbsw.so', 'vendor/lib64/soundfx/libpresetreverbsw.so',
        'vendor/lib/soundfx/libequalizersw.so', 'vendor/lib64/soundfx/libequalizersw.so',
        'vendor/lib/soundfx/libbassboostsw.so', 'vendor/lib64/soundfx/libbassboostsw.so',
        'vendor/lib/soundfx/libnssw.so', 'vendor/lib64/soundfx/libnssw.so',
        'vendor/lib/soundfx/libdownmixaidl.so', 'vendor/lib64/soundfx/libdownmixaidl.so',
        'vendor/lib/soundfx/libreverbaidl.so', 'vendor/lib64/soundfx/libreverbaidl.so',
        'vendor/lib/soundfx/libvisualizeraidl.so', 'vendor/lib64/soundfx/libvisualizeraidl.so',
        'vendor/lib/soundfx/libdynamicsprocessingaidl.so', 'vendor/lib64/soundfx/libdynamicsprocessingaidl.so',
        'vendor/lib/soundfx/libvirtualizersw.so', 'vendor/lib64/soundfx/libvirtualizersw.so',
        'vendor/lib/soundfx/libhapticgeneratoraidl.so', 'vendor/lib64/soundfx/libhapticgeneratoraidl.so',
        'vendor/lib/soundfx/libloudnessenhanceraidl.so', 'vendor/lib64/soundfx/libloudnessenhanceraidl.so',
        'vendor/lib/soundfx/libenvreverbsw.so', 'vendor/lib64/soundfx/libenvreverbsw.so',
        'vendor/lib/soundfx/libaecsw.so', 'vendor/lib64/soundfx/libaecsw.so',
        'vendor/lib/soundfx/libagc2sw.so', 'vendor/lib64/soundfx/libagc2sw.so'
    ): blob_fixup()
        .remove_needed('libaudio_aidl_conversion_common_ndk.so')
        .replace_needed('android.hardware.audio.effect-V2-ndk.so', 'android.hardware.audio.effect-V3-ndk.so')
        .replace_needed('android.media.audio.common.types-V3-ndk.so', 'android.media.audio.common.types-V4-ndk.so')
        .replace_needed('android.hardware.audio.common-V3-ndk.so', 'android.hardware.audio.common-V4-ndk.so'),

    ('vendor/lib64/libmtkcam_hal_aidl_common.so'): blob_fixup()
        .replace_needed('android.hardware.camera.common-V2-ndk.so', 'android.hardware.camera.common-V1-ndk.so'),

    ('vendor/bin/hw/vendor.mediatek.hardware.mtkpower-service.mediatek'): blob_fixup()
        .remove_needed('android.hardware.power-service-mediatek.so'),

    'vendor/lib64/hw/hwcomposer.mtk_common.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),

    (
        'vendor/lib/libteei_daemon_vfs.so',
        'vendor/lib64/libteei_daemon_vfs.so'
    ): blob_fixup()
        .add_needed('liblog.so'),

    ('vendor/bin/hw/android.hardware.contexthub-service.tinysys'): blob_fixup()
        .replace_needed('android.hardware.contexthub-V3-ndk.so', 'android.hardware.contexthub-V4-ndk.so'),

    ('vendor/lib/mt6781/libneuron_adapter_mgvi.so', 'vendor/lib64/mt6781/libneuron_adapter_mgvi.so'): blob_fixup()
        .add_needed('libz.so')
        .add_needed('liblog.so')
        .add_needed('libnativewindow.so')
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_createFromHandle')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_getNativeHandle')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),

    ('vendor/lib64/libalLDC.so', 'vendor/lib64/libalhLDC.so', 'vendor/lib64/libneuralnetworks_sl_driver_mtk_legacy_prebuilt.so'): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_createFromHandle')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_getNativeHandle')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
}

module = ExtractUtilsModule(
    'sea',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
