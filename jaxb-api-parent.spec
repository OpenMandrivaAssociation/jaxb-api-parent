Name:		jaxb-api-parent
Version:	2.4.0
Release:	0.b180830.0359.1
Summary:	JAXB API parent POM
Group:		Development/Java
License:	CDDL-1.1 OR GPL-2.0-only WITH Classpath-exception-2.0
URL:		https://github.com/javaee/jaxb-spec
Source0:	https://repo1.maven.org/maven2/javax/xml/bind/jaxb-api-parent/2.4.0-b180830.0359/jaxb-api-parent-2.4.0-b180830.0359.pom
Source1:	https://raw.githubusercontent.com/javaee/jaxb-spec/2.3.0/LICENSE.txt#/jaxb-api-parent-2.4.0-b180830.0359-LICENSE.txt

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption:	validate

%description
Parent POM for JAXB API 2.4.0-b180830.0359. The API POM inherits the
JavaBeans Activation Framework version from this file. jvnet-parent is
not packaged with it. The dependency management entry is
javax.activation:javax.activation-api 1.2.0.

%prep
cp -p %{SOURCE0} pom.xml
cp -p %{SOURCE1} LICENSE.txt
python - <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def local(tag):
    return tag.split("}", 1)[-1]

tree = ET.parse("pom.xml")
root = tree.getroot()
for node in list(root):
    if local(node.tag) in {"parent", "modules", "build", "profiles"}:
        root.remove(node)
tree.write("pom.xml", encoding="utf-8", xml_declaration=True)
text = Path("pom.xml").read_text(encoding="utf-8")
if "<parent" in text or "jvnet-parent" in text or "<modules" in text:
    raise SystemExit("parent was not removed")
if text.count("<version>2.4.0-b180830.0359</version>") != 1:
    raise SystemExit("maven version changed")
if "<packaging>pom</packaging>" not in text:
    raise SystemExit("packaging is not pom")
if "<activation.version>1.2.0</activation.version>" not in text or "javax.activation-api" not in text:
    raise SystemExit("activation management was dropped")
PY

%files -f .mfiles
%doc LICENSE.txt
