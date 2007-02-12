# TODO
# - initscript.
# - shorter description?
Summary:	Reactive Autonomous Blackhole List (RABL) Project
Summary(pl.UTF-8):   RABL - reaktywna autonomiczna lista "czarnych dziur"
Name:		rabl
Version:	1.0.0
Release:	0.2
Epoch:		0
License:	GPL v2+
Group:		Applications/Mail
Source0:	http://www.nuclearelephant.com/projects/rabl/sources/%{name}_server-%{version}.tar.gz
# Source0-md5:	01614728ef4fa407aec0479dd382eb18
Source1:	http://www.nuclearelephant.com/projects/rabl/sources/%{name}_client-%{version}.tar.gz
# Source1-md5:	4703ead788f62f3d69427b5e0c82faa5
URL:		http://www.nuclearelephant.com/projects/rabl/
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The RABL (pronounced "rabble") server is a statistical,
machine-automated and up-to-the-second blackhole list server designed
to monitor global network activity and make decisions based on network
spread and infection rate - that is, abuse from an address which has
been provided via automated feed from a number of participating
networks. This is in far contrast to how most other blacklists
function, where fallable humans (many with political agendas) must
process thousands of hand-written reports and make decisions - many
times after the fact. The RABL is fully reactive to new threats and
can block addresses within seconds of widespread infection because it
is in constant communication with the participating networks (or
"sources") - good to know in this world of drone PCs and stolen
accounts.

The RABL server blacklists addresses until they have cleared a minimum
duration (an hour by default) without any additional reporting, making
the appeals process as simple as "fix your junk". The RABL is designed
to function via automated machine-learning spam filters, such as
Bayesian filters. Each participating network is granted write
authentication in the blackhole list, to prevent abuse. A client tool
is also provided. Because no humans are involved in this process, the
RABL acts as a mere activity monitor and can run on its own. There's
also nobody to sue (since you can't sue computers for talking to each
other) which makes things far less messy for participants.

%description -l pl.UTF-8
Serwer RABL (Reactive Autonomous Blackhole List) to statystyczny,
zautomatyzowany i aktualny co do sekundy serwer list "czarnych dziur"
zaprojektowany do monitorowania aktywności sieci światowej i
decydowania w oparciu o współczynniki rozprzestrzeniania po sieci i
infekcji - tzn. nadużyć z adresów, które zostały automatycznie
dostarczone z wielu sieci należących do projektu. Różni się to
znacznie od tego, w jaki sposób działa większość innych list "czarnych
dziur", gdzie omylni ludzie (czasem z politycznymi powiązaniami) muszą
przetwarzać tysiące ręcznie pisanych raportów i podejmować decyzje - w
wielu przypadkach po fakcie. RABL jest w pełni reaktywna na nowe
zdarzenia i może blokować adresy w ciągu sekund od szeroko
rozprzestrzenionej infekcji, ponieważ jest w stałej łączności ze
współpracującymi sieciami (lub "źródłami") - co jest dobrą wiadomością
w świecie bezobsługowych pecetów i skradzionych kont.

Serwer RABL trzyma adresy na czarnej liście dopóki nie minie pewien
minimalny czas (domyślnie godzina) bez żadnych dodatkowych raportów,
co sprowadza proces apelacji do "naprawienia swoich śmieci". RABL jest
zaprojektowany do funkcjonowania poprzez automatyczne, uczące się
filtry antyspamowe, takie jak filtry bayesowskie. Każda współpracująca
sieć jest ma uwierzytelniany zapis do listy "czarnych dziur" w celu
zapobiegnięcia nadużyciom. Dostarczone jest także narzędzie klienckie.
Ponieważ w proces nie są zaangażowani ludzie, RABL działa jako
samodzielny monitor aktywności i może funkcjonować samodzielnie. Nie
ma także nikogo do pozwania (ponieważ nie można pozwać komputerów za
rozmawianie między sobą), co czyni działanie mniej kłopotliwym dla
współpracujących.

%package server
Summary:	Reactive Autonomous Blackhole List server
Summary(pl.UTF-8):   Serwer RABL (reaktywnej autonomicznej listy "czarnych dziur")
Group:		Applications/Mail
%if %{with initscript}
Requires(post,preun):	rc-scripts
Requires(post,preun):	/sbin/chkconfig
%endif

%description server
The RABL server is the server component of the blacklist. It is only
necessary to use the server if you are running your own local RABL. If
you are looking to simply subscribe to the public RABL, then you need
the RABL client instead.

%description server -l pl.UTF-8
Serwer RABL to część serwerowa czarnych list. Jest wymagana tylko do
używania serwera własnej lokalnej RABL. Aby po prostu zapisać się do
publicznej RABL potrzebny jest klient RABL.

%package client
Summary:	Reactive Autonomous Blackhole List client
Summary(pl.UTF-8):   Klient RABL (reaktywnej autonomicznej listy "czarnych dziur")
Group:		Applications/Mail

%description client
The RABL client is the lookup and reporting component of the RABL. It
is necessary for performing streaming connection lookups and writing
to the RABL (assuming you have an account).

%description client -l pl.UTF-8
Klient RABL to część RABL służąca do sprawdzania i raportowania. Jest
potrzebny do sprawdzanai połączeń strumieniowych i zapisu do RABL (w
przypadku posiadania konta).

%prep
%setup -q -c -T -a0 -a1
mv %{name}_server-%{version} server
mv %{name}_client-%{version} client

%build
cd server
%configure
%{__make}

cd ../client
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C server install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C client install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with initscript}
%post server
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun server
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files server
%defattr(644,root,root,755)
%doc server/{CHANGE,README,RELEASE.NOTES,rabl_server.conf}
%attr(755,root,root) %{_bindir}/rabl_server

%files client
%defattr(644,root,root,755)
%doc client/{CHANGE,README,RELEASE.NOTES,rabl_client.conf}
%attr(755,root,root) %{_bindir}/rabl_client
