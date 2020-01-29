cmake_minimum_required(VERSION 3.2)
project(freeimage LANGUAGES CXX C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package ( ZLIB REQUIRED )

set(freeimage_SOURCES
    "Source/FreeImage/BitmapAccess.cpp"
    "Source/FreeImage/ColorLookup.cpp"
    "Source/FreeImage/ConversionRGBA16.cpp"
    "Source/FreeImage/ConversionRGBAF.cpp"
    "Source/FreeImage/FreeImage.cpp"
    "Source/FreeImage/FreeImageIO.cpp"
    "Source/FreeImage/GetType.cpp"
    "Source/FreeImage/LFPQuantizer.cpp"
    "Source/FreeImage/MemoryIO.cpp"
    "Source/FreeImage/PixelAccess.cpp"
    "Source/FreeImage/NNQuantizer.cpp"
    "Source/FreeImage/WuQuantizer.cpp"
    "Source/FreeImage/Conversion.cpp"
    "Source/FreeImage/Conversion16_555.cpp"
    "Source/FreeImage/Conversion16_565.cpp"
    "Source/FreeImage/Conversion24.cpp"
    "Source/FreeImage/Conversion32.cpp"
    "Source/FreeImage/Conversion4.cpp"
    "Source/FreeImage/Conversion8.cpp"
    "Source/FreeImage/ConversionFloat.cpp"
    "Source/FreeImage/ConversionRGB16.cpp"
    "Source/FreeImage/ConversionRGBF.cpp"
    "Source/FreeImage/ConversionType.cpp"
    "Source/FreeImage/ConversionUINT16.cpp"
    "Source/FreeImage/Halftoning.cpp"
    "Source/FreeImage/tmoColorConvert.cpp"
    "Source/FreeImage/tmoDrago03.cpp"
    "Source/FreeImage/tmoFattal02.cpp"
    "Source/FreeImage/tmoReinhard05.cpp"
    "Source/FreeImage/ToneMapping.cpp"
    "Source/FreeImage/J2KHelper.cpp"
    "Source/FreeImage/MNGHelper.cpp"
    "Source/FreeImage/Plugin.cpp"
    "Source/FreeImage/PluginBMP.cpp"
    "Source/FreeImage/PluginCUT.cpp"
    "Source/FreeImage/PluginDDS.cpp"
    "Source/FreeImage/PluginEXR.cpp"
    "Source/FreeImage/PluginG3.cpp"
    "Source/FreeImage/PluginGIF.cpp"
    "Source/FreeImage/PluginHDR.cpp"
    "Source/FreeImage/PluginICO.cpp"
    "Source/FreeImage/PluginIFF.cpp"
    "Source/FreeImage/PluginJ2K.cpp"
    "Source/FreeImage/PluginJNG.cpp"
    "Source/FreeImage/PluginJP2.cpp"
    "Source/FreeImage/PluginJPEG.cpp"
    # "Source/FreeImage/PluginJXR.cpp"
    "Source/FreeImage/PluginKOALA.cpp"
    "Source/FreeImage/PluginMNG.cpp"
    "Source/FreeImage/PluginPCD.cpp"
    "Source/FreeImage/PluginPCX.cpp"
    "Source/FreeImage/PluginPFM.cpp"
    "Source/FreeImage/PluginPICT.cpp"
    "Source/FreeImage/PluginPNG.cpp"
    "Source/FreeImage/PluginPNM.cpp"
    "Source/FreeImage/PluginPSD.cpp"
    "Source/FreeImage/PluginRAS.cpp"
    "Source/FreeImage/PluginRAW.cpp"
    "Source/FreeImage/PluginSGI.cpp"
    "Source/FreeImage/PluginTARGA.cpp"
    "Source/FreeImage/PluginTIFF.cpp"
    "Source/FreeImage/PluginWBMP.cpp"
    "Source/FreeImage/PluginWebP.cpp"
    "Source/FreeImage/PluginXBM.cpp"
    "Source/FreeImage/PluginXPM.cpp"
    "Source/FreeImage/PSDParser.cpp"
    "Source/FreeImage/TIFFLogLuv.cpp"
    "Source/FreeImage/CacheFile.cpp"
    "Source/FreeImage/MultiPage.cpp"
    "Source/FreeImage/ZLibInterface.cpp"
    "Source/Metadata/Exif.cpp"
    "Source/Metadata/FIRational.cpp"
    "Source/Metadata/FreeImageTag.cpp"
    "Source/Metadata/IPTC.cpp"
    "Source/Metadata/TagConversion.cpp"
    "Source/Metadata/TagLib.cpp"
    "Source/Metadata/XTIFF.cpp"
    "Source/FreeImageToolkit/Background.cpp"
    "Source/FreeImageToolkit/BSplineRotate.cpp"
    "Source/FreeImageToolkit/Channels.cpp"
    "Source/FreeImageToolkit/ClassicRotate.cpp"
    "Source/FreeImageToolkit/Colors.cpp"
    "Source/FreeImageToolkit/CopyPaste.cpp"
    "Source/FreeImageToolkit/Display.cpp"
    "Source/FreeImageToolkit/Flip.cpp"
    "Source/FreeImageToolkit/JPEGTransform.cpp"
    "Source/FreeImageToolkit/MultigridPoissonSolver.cpp"
    "Source/FreeImageToolkit/Rescale.cpp"
    "Source/FreeImageToolkit/Resize.cpp"
    "Source/transupp.c"
)


if(MSVC)
    set(freeimage_SOURCES
        ${freeimage_SOURCES}
        "FreeImage.rc"
        )
endif(MSVC)

include_directories("Source") 
add_library(freeimage SHARED ${freeimage_SOURCES})

if(MSVC)
    target_link_libraries(freeimage ${CONAN_LIBS})
    target_compile_definitions(freeimage PUBLIC FREEIMAGE_EXPORTS _CRT_SECURE_NO_WARNINGS)
else(MSVC)
    target_link_libraries(freeimage ${CONAN_LIBS_LIBJPEG} ${CONAN_LIBS_OPENJPEG})
endif(MSVC)

