#
# Conditional build:
%bcond_with	tests	# unit tests (not included in sdist)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Checks CloudFormation templates for practices and behaviour that could potentially be improved
Summary(pl.UTF-8):	Sprawdzanie szablonów CloudFormation pod kątem praktyk i zachowania do poprawny
Name:		python-cfn-lint
# keep 0.56.x here for python2 support
Version:	0.56.4
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cfn-lint/
Source0:	https://files.pythonhosted.org/packages/source/c/cfn-lint/cfn-lint-%{version}.tar.gz
# Source0-md5:	ba0ec3f6e7087fd4aa940abb774b9d3b
Patch0:		cfn-lint-requirements.patch
URL:		https://pypi.org/project/cfn-lint/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 5.4.1
BuildRequires:	python-aws-sam-translator >= 1.42.0
BuildRequires:	python-importlib_resources >= 1.4
BuildRequires:	python-jsonpatch
BuildRequires:	python-jsonschema >= 3.0
BuildRequires:	python-jschema_to_python >= 1.2.3
BuildRequires:	python-junit-xml >= 1.9
BuildRequires:	python-networkx < 2.3
BuildRequires:	python-pathlib2 >= 2.3.0
BuildRequires:	python-pyrsistent < 0.17
BuildRequires:	python-sarif-om >= 1.0.4
BuildRequires:	python-six >= 1.11
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 5.4.1
BuildRequires:	python3-aws-sam-translator >= 1.42.0
%if "%{py3_ver}" == "3.6"
BuildRequires:	python3-importlib_resources >= 1.4
%endif
BuildRequires:	python3-jsonpatch
BuildRequires:	python3-jsonschema >= 3.0
BuildRequires:	python3-jschema_to_python >= 1.2.3
BuildRequires:	python3-junit-xml >= 1.9
BuildRequires:	python3-networkx >= 2.4
BuildRequires:	python3-sarif-om >= 1.0.4
BuildRequires:	python3-six >= 1.11
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
# replace with other requires if defined in setup.py
Requires:	python-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Validate AWS CloudFormation yaml/json templates against the AWS
CloudFormation Resource Specification
<https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html>
and additional checks. Includes checking valid values for resource
properties and best practices.

%description -l pl.UTF-8
Sprawdzanie poprawności szablonów yaml/json AWS CloudFormation
względem specyfikacji zasobów AWS CloudFormation:
<https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html>
i pod kątem innych aspektów. Zawiera sprawdzanie poprawnych wartości
własności zasobów i dobrych praktyk.

%package -n python3-cfn-lint
Summary:	Checks CloudFormation templates for practices and behaviour that could potentially be improved
Summary(pl.UTF-8):	Sprawdzanie szablonów CloudFormation pod kątem praktyk i zachowania do poprawny
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-cfn-lint
Validate AWS CloudFormation yaml/json templates against the AWS
CloudFormation Resource Specification
<https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html>
and additional checks. Includes checking valid values for resource
properties and best practices.

%description -n python3-cfn-lint -l pl.UTF-8
Sprawdzanie poprawności szablonów yaml/json AWS CloudFormation
względem specyfikacji zasobów AWS CloudFormation:
<https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html>
i pod kątem innych aspektów. Zawiera sprawdzanie poprawnych wartości
własności zasobów i dobrych praktyk.

%prep
%setup -q -n cfn-lint-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/cfn-lint{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/cfn-lint{,-3}
ln -sf cfn-lint-3 $RPM_BUILD_ROOT%{_bindir}/cfn-lint
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE NOTICE README.md
%attr(755,root,root) %{_bindir}/cfn-lint-2
%{py_sitescriptdir}/cfnlint
%{py_sitescriptdir}/cfn_lint-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-cfn-lint
%defattr(644,root,root,755)
%doc LICENSE NOTICE README.md
%attr(755,root,root) %{_bindir}/cfn-lint
%attr(755,root,root) %{_bindir}/cfn-lint-3
%{py3_sitescriptdir}/cfnlint
%{py3_sitescriptdir}/cfn_lint-%{version}-py*.egg-info
%endif
