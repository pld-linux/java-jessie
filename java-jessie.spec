# TODO:
# - build provider (see %%build section)
# - javadoc
# NOTE:
# - it is possible to build it using java-sun, but sun's JRE provides better
#   implementation of JSSE. This package is a JSSE replacemnt for alternative
#   JREs, like java-gcj-compat.

# Conditional build
%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%include	/usr/lib/rpm/macros.java
#
%define		srcname	jessie
Summary:	A free implementation of the JSSE
Summary(pl.UTF-8):	Wolna implementacja JSSE
Name:		java-jessie
Version:	1.0.1
Release:	2
License:	GPL v2
Group:		Libraries/Java
Source0:	http://syzygy.metastatic.org/jessie/jessie-%{version}.tar.gz
# Source0-md5:	c14db8483ca9fae428b8497659861ef0
URL:		http://www.nongnu.org/jessie/
BuildRequires:	ant
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	java-gnu-classpath
BuildRequires:	java-gnu-crypto >= 2.0.1
BuildRequires:	jpackage-utils >= 0:1.6
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Provides:	jsse = 1.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jessie is a free, clean-room implementation of the Java Secure Sockets
Extension, the JSSE. It provides the core API for programming network
sockets with the Secure Socket Layer (SSL), which creates an
authenticated, unforgeable, and protected layer around network
communications. Its goal is to be a drop-in package for free Java
class libraries such as Classpath and its derivatives, and is being
written to depend only on free software, and only with the API
specification and the public protocol specifications.

%prep
%setup -q -n jessie-%{version}

%build
%ant clean
%ant jsse.jar

# Does not build
%if %{with provider}
%ant compile-provider
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a jsse.jar $RPM_BUILD_ROOT%{_javadir}/jsse-%{version}.jar
ln -s jsse-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jsse.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS FAQ NEWS README THANKS TODO
%{_javadir}/*.jar
