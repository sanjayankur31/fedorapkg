%global octpkg zmat

Name:           octave-%{octpkg}
Version:        0.8
Release:        1%{?dist}
Summary:        ZMAT: A portable data compression/decompression toolbox for MATLAB/Octave
License:        GPLv3+ or BSD
URL:            https://github.com/fangq/zmat
Source0:        https://github.com/fangq/zmat/archive/v%{version}/%{octpkg}-%{version}.tar.gz
Source1:        https://github.com/lloyd/easylzma/archive/0.0.7.tar.gz
BuildArch:      noarch
BuildRequires:  cmake, octave-devel

Requires:       octave
Requires(post): octave
Requires(postun): octave

%description
ZMat is a portable mex function to enable zlib/gzip/lzma/lzip/lz4/lz4hc based data 
compression/decompression and base64 encoding/decoding support in MATLAB and GNU Octave. 
It is fast and compact, can process a large array within a fraction of a second.
Among the 6 supported compression methods, lz4 is the fastest for 
compression/decompression; lzma is the slowest but has the highest compression 
ratio; zlib/gzip have the best balance between speed and compression time.

%prep
%autosetup -n %{octpkg}-%{version}

cp LICENSE.txt COPYING

cat > DESCRIPTION << EOF
Name: %{octpkg}
Version: %{version}
Date: %(date +"%Y-%d-%m")
Title: %{summary}
Author: Qianqian Fang <fangqq@gmail.com>
Maintainer: Qianqian Fang <fangqq@gmail.com>
Description: ZMat is a portable mex function to enable zlib/gzip/lzma/lzip/lz4/lz4hc based data 
compression/decompression and base64 encoding/decoding support in MATLAB and GNU Octave. 
It is fast and compact, can process a large array within a fraction of a second.
Among the 6 supported compression methods, lz4 is the fastest for 
compression/decompression; lzma is the slowest but has the highest compression 
ratio; zlib/gzip have the best balance between speed and compression time.

Categories: Zip
EOF

cat > INDEX << EOF
jsonlab >> ZMat
ZMat
 zmat
EOF

mkdir -p inst/
mv *.m inst/

%build
cd src/
wget https://github.com/lloyd/easylzma/archive/0.0.7.tar.gz
tar zxvf 0.0.7.tar.gz
rm -rf easylzma
mv easylzma-0.0.7 easylzma
cd easylzma
cmake .
make
mv easylzma-0.0.7 easylzma-0.0.8
cd ../
make clean 
make oct
cd ../
mv *.mex inst/
%octave_pkg_build

%install
%octave_pkg_install

%post
%octave_cmd pkg rebuild

%preun
%octave_pkg_preun

%postun
%octave_cmd pkg rebuild

%files
%license LICENSE.txt
%doc examples
%dir %{octpkgdir}
%{octpkgdir}/*.m
%{octpkgdir}/*.mex
%doc %{octpkgdir}/doc-cache
%{octpkgdir}/packinfo

%changelog
* Thu Oct 01 2019 Qianqian Fang <fangqq@gmail.com> - 0.8-1
- Initial package
