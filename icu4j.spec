%{?scl:%scl_package icu4j}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

Name:           %{?scl_prefix}icu4j
Version:        54.1.1
Release:        8.%{baserelease}%{?dist}
Epoch:          1
Summary:        International Components for Unicode for Java
License:        MIT and EPL
URL:            http://site.icu-project.org/

#CAUTION
#to create a tarball use following procedure
#svn co http://source.icu-project.org/repos/icu/icu4j/tags/release-54-1-1 icu4j-<version>
#tar caf icu4j-<version>.tar.xz icu4j-<version>/
Source0:        icu4j-%{version}.tar.xz

# Java 8 taglet API changes
Patch0:         java8-taglets.patch

# Add better OSGi metadata to core jar
Patch1:         improve-osgi-manifest.patch

BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  java-javadoc
BuildRequires:  %{?scl_prefix_maven}javapackages-local
BuildRequires:  zip

# Obsoletes/provides added in F22
Obsoletes:      %{name}-eclipse < %{epoch}:%{version}-%{release}
Provides:       %{name}-eclipse = %{epoch}:%{version}-%{release}

BuildArch:      noarch

%description
The International Components for Unicode (ICU) library provides robust and
full-featured Unicode services on a wide variety of platforms. ICU supports
the most current version of the Unicode standard, and provides support for
supplementary characters (needed for GB 18030 repertoire support).

Java provides a very strong foundation for global programs, and IBM and the
ICU team played a key role in providing globalization technology into Sun's
Java. But because of its long release schedule, Java cannot always keep
up-to-date with evolving standards. The ICU team continues to extend Java's
Unicode and internationalization support, focusing on improving
performance, keeping current with the Unicode standard, and providing
richer APIs, while remaining as compatible as possible with the original
Java text and internationalization API design.

%package charset
Summary:        Charset converter library of %{pkg_name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description charset
Charset converter library of %{pkg_name}.

%package localespi
Summary:        Locale SPI library of %{pkg_name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description localespi
Locale SPI library of %{pkg_name}.

%package javadoc
Summary:        Javadoc for %{pkg_name}
Requires:       java-javadoc

%description javadoc
API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n icu4j-%{version}

%patch0
%patch1

# Disable doclinting
sed -i '/additionalparam/ s/additionalparam="/additionalparam="-Xdoclint:none /' build.xml
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
export JAVA_HOME=%{_jvmdir}/java/
ant -Dicu4j.api.doc.jdk.link=%{_javadocdir}/java all check

%mvn_artifact pom.xml icu4j.jar
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install -J doc

# No poms for these, so install manually
install -m 644 icu4j-charset.jar   %{buildroot}%{_javadir}/icu4j/
install -m 644 icu4j-localespi.jar %{buildroot}%{_javadir}/icu4j/
%{?scl:EOF}


%files -f .mfiles
%doc main/shared/licenses/license.html readme.html APIChangeReport.html
%dir %{_javadir}/icu4j
%dir %{_mavenpomdir}/icu4j

%files charset
%doc main/shared/licenses/license.html
%{_javadir}/icu4j/icu4j-charset.jar

%files localespi
%doc main/shared/licenses/license.html
%{_javadir}/icu4j/icu4j-localespi.jar

%files javadoc -f .mfiles-javadoc
%doc main/shared/licenses/license.html

%changelog
* Thu Jul 21 2016 Mat Booth <mat.booth@redhat.com> - 1:54.1.1-8.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Jul 21 2016 Mat Booth <mat.booth@redhat.com> - 1:54.1.1-8
- Disable doclinting during javadoc generation

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:54.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 22 2015 Mat Booth <mat.booth@redhat.com> - 1:54.1.1-6
- Remove incomplete SCL macros

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:54.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 21 2014 Mat Booth <mat.booth@redhat.com> - 1:54.1.1-4
- Drop unnecessay requires on main package and fix requires on sub packages

* Fri Nov 21 2014 Mat Booth <mat.booth@redhat.com> - 1:54.1.1-3
- Drop the eclipse sub-package, no longer needed

* Mon Nov 17 2014 Mat Booth <mat.booth@redhat.com> - 1:54.1.1-2
- Fix typo in osgi manifest patch

* Mon Nov 17 2014 Mat Booth <mat.booth@redhat.com> - 1:54.1.1-1
- Update to latest upstream release
- Add patch for building against java 8 taglet API
  - Fixes: rhbz#1087450, rhbz#1106794
- Add patch for generating better OSGi metadata in core lib
- Install core lib with mvn_install
- Package localespi lib
- Run test suite

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:52.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1:52.1-2
- Use Requires: java-headless rebuild (#1067528)

* Tue Mar 18 2014 Michael Simacek <msimacek@redhat.com> - 1:52.1-1
- Update to upstream version 52.1
- Require java-headless

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:50.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.1-1
- Update to latest upstream.

* Fri Mar 22 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-7
- Build sclized version using SCLized Eclipse.

* Thu Feb 21 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-6
- RHBZ#913369 Provide icu4j-charset library

* Tue Feb 12 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-5
- SCLize.

* Mon Feb 11 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-4
- Revert a hardcoded path.

* Mon Feb 11 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-3
- Complete the removal.

* Mon Feb 11 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-2
- Remove the main jar manifest.

* Thu Feb 7 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-1
- Update to latest upstream. 

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.2.2-12
- Don't build icu4j-eclipse for rhel.

* Thu Feb 16 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2.2-11
- Make the package noarch.

* Wed Feb  1 2012 Daniel Mach <dmach@redhat.com> 1:4.4.2.2-10
- Tweak with_eclipse macro for rhel and non-intel architectures.

* Fri Jan 27 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2.2-9
- Getting back to 4 digit version

* Thu Jan 26 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2-8
- Proper sources uploaded

* Thu Jan 26 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2-7
- Better versioning consistent with previous releases

* Mon Jan 16 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2.2-6
- Update to 4.4.2.2.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.2-4
- Add proper manifest to the jar in the main package.

* Fri Sep 16 2011 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.2-3
- Adapt to current guidelines.

* Mon May 9 2011 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.2-2
- Use proper tarball.
- Fix build.

* Tue Apr 05 2011 Chris Aniszczyk <zx@redhat.com> 1:4.4.2-1
- Update to 4.4.2.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 8 2010 Alexander Kurtakov <akurtako@redhat.com> 1:4.2.1-1
- Update to 4.2.1.

* Fri Feb  5 2010 Mary Ellen Foster <mefoster at gmail.com> 1:4.0.1-5
- Add maven pom and depmap fragment

* Tue Sep 29 2009 Alexander Kurtakov <akurtako@redhat.com> 1:4.0.1-4
- Simplify with_eclipse conditional.

* Mon Aug 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1:4.0.1-3
- Update qualifier to the Eclipse 3.5.0 release.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 8 2009 Alexander Kurtakov <akurtako@redhat.com> 1:4.0.1-1
- Update to 4.0.1.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct  8 2008 Ville Skyttä <ville.skytta at iki.fi> - 0:3.8.1-4
- Disable debuginfo package when built with Eclipse support, change to
  noarch when built without it (#464017).

* Mon Aug 11 2008 Andrew Overholt <overholt@redhat.com> 3.8.1-3
- Get rid of eclipse_name macro
- Rebuild with Eclipse 3.4 and put into Eclipse stuff into
  %%{_libdir}/eclipse
- Remove now-unnecessary OSGi configuration dir patch
- Add patch to point to PDE Build location

* Fri Jul 11 2008 Andrew Overholt <overholt@redhat.com> 0:3.8.1-2
- Remove GCJ support due to
  com.sun.tools.doclets.internal.toolkit.taglets.* import (not in gjdoc)

* Fri Jul 11 2008 Andrew Overholt <overholt@redhat.com> 0:3.8.1-1
- 3.8.1

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:3.6.1-3
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:3.6.1-2jpp.6
- Autorebuild for GCC 4.3

* Tue Nov 13 2007 Andrew Overholt <overholt@redhat.com> 3.6.1-1jpp.6
- Bump release and change updatetimestamp patch to have DOS
  line-endings.

* Tue Nov 13 2007 Andrew Overholt <overholt@redhat.com> 3.6.1-1jpp.5
- Bump release.

* Fri Sep 28 2007 Andrew Overholt <overholt@redhat.com> 3.6.1-1jpp.4
- Update timestamp to match Eclipse 3.3.1 release.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.6.1-1jpp.3
- Rebuild for selinux ppc32 issue.

* Wed Jun 27 2007 Ben Konrath <bkonrath@redhat.com> - 0:3.6.1-1jpp.2
- Remove requires eclipse-rcp in eclipse sub-package.

* Thu Jun 07 2007 Ben Konrath <bkonrath@redhat.com> - 0:3.6.1-1jpp.1
- 3.6.1.
- Enable eclipse sub-package.

* Fri Mar 16 2007 Jeff Johnston <jjohnstn@redhat.com> - 0:3.4.5-2jpp.2
- Disable eclipse plugin support temporarily until build problems
  can be worked out.  Plugin is still being built as part of
  eclipse platform.
- BuildRequire sinjdoc.

* Mon Feb 12 2007 Matt Wringe <mwringe@redhat.com> - 0:3.4.5-2jpp.1
- Fix some rpmlint issues
- Make use of buildroot more consistent
- Remove javadoc post and postun sections as per new jpp standard
- Change license section to 'MIT style' license from 'MIT' license.
  This was done since the source package calls the license the 
  "X license" (see readme.html in src jar).
- Install eclipse plugin into /usr/share/eclipse

* Mon Jan 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.4.5-2jpp.1
- Merge with upstream

* Mon Jan 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.4.5-2jpp
- Add optional eclipse subpackage, created by
  Jeff Johnston  <jjohnstn@rdhat.com> :
- Add eclipse sub-package to create plugins.

* Mon Jan 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.4.5-1jpp
- Upgrade to 3.4.5 with merge
- Re-enable javadoc

* Mon Sep 04 2006 Ben Konrath <bkonrath@redhat.com> 0:3.4.5-1jpp_1fc
- 3.4.5.
- Add GCJ support with spec-convert-gcj-1.6.

* Mon Jul 17 2006 Ben Konrath <bkonrath@redhat.com> 0:3.4.4-1jpp_1fc
- 3.4.4.
- Add disable javadocs patch.

* Tue Feb 28 2006 Fernando Nasser <fnasser@redhat.com> - 0:3.2-2jpp_1rh
- First Red Hat build

* Mon Feb 27 2006 Fernando Nasser <fnasser@redhat.com> - 0:3.2-2jpp
- First JPP 1.7 build

* Sat Jan 29 2005 David Walluck <david@jpackage.org> 0:3.2-1jpp
- release (contributed by Mary Ellen Foster <mefoster at gmail.com>)