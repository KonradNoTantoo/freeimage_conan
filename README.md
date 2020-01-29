# Conan recipe for freeimage 3.18.0

[![Build Status: Windows](https://ci.appveyor.com/api/projects/status/github/KonradNoTantoo/freeimage_conan?svg=true)](https://ci.appveyor.com/project/KonradNoTantoo/freeimage-conan)

[![Build Status: Linux](https://api.travis-ci.org/KonradNoTantoo/freeimage_conan.svg?branch=master)](https://travis-ci.org/KonradNoTantoo/freeimage_conan)

### Description
A test recipe for now...

### Repository
Published on [Utopia bintray](https://bintray.com/konradnotantoo/utopia/):
```
conan remote add utopia https://api.bintray.com/conan/konradnotantoo/utopia
```

### Recipe license
GPLv2

Parts of the current recipe (specifically the files inside the patches directory) and most of the hacks in the recipe were stolen from Gentoo (see the [ebuild here](https://gitweb.gentoo.org/repo/gentoo.git/tree/media-libs/freeimage)). It is probably safer to licence the recipe under GPLv2, however annoying that infectious license can be, in our current and very narrow case. It's not like anybody here is getting rich by sucking out some other developper's intellectual property, right? However, as annoyed as I am by licensing issues, I must humbly thank the authors of those Gentoo patches, since I would probably have abandonned this recipe without their prior, and most efficient, work.