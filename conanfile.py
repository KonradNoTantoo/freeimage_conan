from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
import os
import shutil
import glob



class FreeimageConan(ConanFile):
    name = "freeimage"
    version = "3.18.0"
    compact_version = version.replace('.', '')
    folder_name = "FreeImage"
    license = "GPLv2"
    author = "konrad.no.tantoo"
    url = "https://github.com/KonradNoTantoo/freeimage_conan"
    description = "FreeImage is an Open Source library project for developers who would like to support popular graphics image formats like PNG, BMP, JPEG, TIFF and others as needed by today's multimedia applications."
    topics = ("conan", "image decoding", "graphics")
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "with_exr": [True,False],
        "with_jpeg": [True,False],
        "with_jpeg2k": [True,False],
        "with_mng": [True,False],
        "with_png": [True,False],
        "with_tiff": [True,False],
        "with_raw": [True,False],
        "with_webp": [True,False],
    }

    default_options = {
        "with_exr": True,
        "with_jpeg": True,
        "with_jpeg2k": True,
        "with_mng": True,
        "with_png": True,
        "with_tiff": True,
        "with_raw": True,
        "with_webp": True,
    }

    generators = "cmake"
    exports = ["CMakeLists.txt", os.path.join("patches", "*")]

    def copy_file_to_source(self, name):
        file_content = tools.load(name)
        path_to_source = os.path.join(self.source_folder, self.folder_name, name)
        tools.save(path_to_source, file_content)

    def requirements(self):
        self.requires("zlib/1.2.11@conan/stable")

        if self.options.with_jpeg:
            self.requires("libjpeg/9c@bincrafters/stable")
        if self.options.with_jpeg2k:
            self.requires("openjpeg/2.3.0@bincrafters/stable")
        if self.options.with_png:
            self.requires("libpng/1.6.36@bincrafters/stable")
        if self.options.with_tiff:
            self.requires("libtiff/4.0.9@bincrafters/stable")
        if self.options.with_webp:
            self.requires("libwebp/1.0.0@bincrafters/stable")
        if self.options.with_exr:
            self.requires("openexr/2.3.0@conan/stable")
        if self.options.with_raw:
            self.requires("libraw/0.19.5@utopia/testing")

    def source(self):
        tarball_path = "http://downloads.sourceforge.net/freeimage/FreeImage{}.zip".format(self.compact_version)
        tools.get(tarball_path)
        sources_path = os.path.join(self.folder_name, "Source")

        # save needed headers
        needed_headers = [
            ["LibJPEG", "transupp.c"],
            ["LibJPEG", "transupp.h"],
            ["LibJPEG", "jinclude.h"],
            ["LibTIFF4", "tiffiop.h"],
            ["LibTIFF4", "tif_dir.h"],
        ]
        for header in needed_headers:
            target = os.path.join(sources_path, header[-1])
            header = os.path.join(sources_path, *header)
            self.output.info("Saving header file: {}".format(header))
            shutil.move(header, target)

        packaged_dependencies = [
                "LibJPEG",
                "LibJXR",
                "LibPNG",
                "LibTIFF4",
                "ZLib",
                "LibOpenJPEG",
                "OpenEXR",
                "LibRawLite",
                "LibWebP",
                # "LibMNG",
            ]
        for directory in packaged_dependencies:
            target_path = os.path.join(sources_path, directory)
            self.output.info("Deleting packaged dependency: {}".format(target_path))
            shutil.rmtree(target_path)

        # change line ends for patch to work
        files_to_edit = []
        file_patterns = [
            "Makefile.*",
            "fipMakefile.srcs",
            "*/*.h",
            "*/*/*.cpp",
        ]
        for pattern in file_patterns:
            files_to_edit.extend(glob.glob("{}/{}".format(self.folder_name, pattern)))

        for file in files_to_edit:
            tools.dos2unix(file)

        count_operations = 1
        edited_files = ["Makefile.srcs", "fipMakefile.srcs"]
        for file in edited_files:
            self.output.info("Editing file: {} [{}/{}]".format(file, count_operations, len(edited_files)))
            count_operations += 1
            file = "{}/{}".format(self.folder_name, file)
            tools.replace_in_file(file, "/./", "/", strict=False)
            tools.replace_in_file(file, " ./", " ", strict=False)
            tools.replace_in_file(file, " Source", " \\\n\tSource", strict=False)
            tools.replace_in_file(file, " Wrapper", " \\\n\tWrapper", strict=False)
            tools.replace_in_file(file, " Examples", " \\\n\tExamples", strict=False)
            tools.replace_in_file(file, " TestAPI", " \\\n\tTestAPI", strict=False)
            tools.replace_in_file(file, " -ISource", " \\\n\t-ISource", strict=False)
            tools.replace_in_file(file, " -IWrapper", " \\\n\t-IWrapper", strict=False)
            tools.replace_in_file(file, "INCLS", "\nINCLS", strict=False)

            exclude_filter = [
                "LibJPEG",
                "LibJXR",
                "LibPNG",
                "LibTIFF",
                "Source/ZLib",
                "LibOpenJPEG",
                "OpenEXR",
                "LibRawLite",
                "LibMNG",
                "LibWebP",
                "LibJXR",
                ]
            with open(file) as oldfile, open("tmpfile", 'w') as newfile:
                for line in oldfile:
                    if not any(exclude in line for exclude in exclude_filter):
                        newfile.write(line)
            shutil.move("tmpfile", file)

        patches=[
            "freeimage-3.18.0-unbundling.patch",
            "freeimage-3.18.0-remove-jpeg-transform.patch",
            "freeimage-3.18.0-rename-jpeg_read_icc_profile.patch",
            "freeimage-3.18.0-disable-plugin-G3.patch",
            "freeimage-3.18.0-raw.patch",
            "freeimage-3.18.0-libjpeg9.patch",
        ]
        count_operations = 1
        for patch in patches:
            self.output.info("Applying patch: {} [{}/{}]".format(patch, count_operations, len(patches)))
            count_operations += 1
            tools.patch(base_path=self.folder_name, patch_file=os.path.join("patches", patch))

        # TODO make that into a patch
        tools.replace_in_file(os.path.join(sources_path, "transupp.c"), "FMEMZERO", "MEMZERO")

        self.copy_file_to_source("CMakeLists.txt")


    def build(self):
        # install custom CMakeLists in source and use CMake
        cmake = CMake(self)

        cmake.definitions["WITH_EXR"] = "ON" if self.options.with_exr else "OFF"
        cmake.definitions["WITH_JPEG"] = "ON" if self.options.with_jpeg else "OFF"
        cmake.definitions["WITH_JPEG2K"] = "ON" if self.options.with_jpeg2k else "OFF"
        cmake.definitions["WITH_MNG"] = "ON" if self.options.with_mng else "OFF"
        cmake.definitions["WITH_PNG"] = "ON" if self.options.with_png else "OFF"
        cmake.definitions["WITH_TIFF"] = "ON" if self.options.with_tiff else "OFF"
        cmake.definitions["WITH_RAW"] = "ON" if self.options.with_raw else "OFF"
        cmake.definitions["WITH_WEBP"] = "ON" if self.options.with_webp else "OFF"

        cmake.configure(source_folder=self.folder_name)
        cmake.build()


    def package(self):
        self.copy("Source/CacheFile.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/MapIntrospector.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/Metadata/FIRational.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/FreeImage.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/FreeImageIO.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/Metadata/FreeImageTag.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/Plugin.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/FreeImage/PSDParser.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/Quantizers.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/ToneMapping.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/Utilities.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("Source/FreeImageToolkit/Resize.h", dst="include", src=self.folder_name, keep_path=False)
        self.copy("*/freeimage.dll", dst="bin", keep_path=False)
        self.copy("*/libfreeimage.so", dst="lib", keep_path=False)
        self.copy("lib/*.pdb", dst="lib", keep_path=False)
        self.copy("lib/*.exp", dst="lib", keep_path=False)
        self.copy("lib/*.lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["freeimage"]

