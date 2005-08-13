# TODO
# - initscript.
# - shorter description?
Summary:	Reactive Autonomous Blackhole List (RABL) Project
Summary(pl):	RABL - reaktywna autonomiczna lista "czarnych dziur"
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

%description -l pl
Serwer RABL (Reactive Autonomous Blackhole List) to statystyczny,
zautomatyzowany i aktualny co do sekundy serwer list "czarnych dziur"
zaprojektowany do monitorowania aktywno�ci sieci �wiatowej i
decydowania w oparciu o wsp�czynniki rozprzestrzeniania po sieci i
infekcji - tzn. nadu�y� z adres�w, kt�re zosta�y automatycznie
dostarczone z wielu sieci nale��cych do projektu. R�ni si� to
znacznie od tego, w jaki spos�b dzia�a wi�kszo�� innych list "czarnych
dziur", gdzie omylni ludzie (czasem z politycznymi powi�zaniami) musz�
przetwarza� tysi�ce r�cznie pisanych raport�w i podejmowa� decyzje - w
wielu przypadkach po fakcie. RABL jest w pe�ni reaktywna na nowe
zdarzenia i mo�e blokowa� adresy w ci�gu sekund od szeroko
rozprzestrzenionej infekcji, poniewa� jest w sta�ej ��czno�ci ze
wsp�pracuj�cymi sieciami (lub "�r�d�ami") - co jest dobr� wiadomo�ci�
w �wiecie bezobs�ugowych pecet�w i skradzionych kont.

Serwer RABL trzyma adresy na czarnej li�cie dop�ki nie minie pewien
minimalny czas (domy�lnie godzina) bez �adnych dodatkowych raport�w,
co sprowadza proces apelacji do "naprawienia swoich �mieci". RABL jest
zaprojektowany do funkcjonowania poprzez automatyczne, ucz�ce si�
filtry antyspamowe, takie jak filtry bayesowskie. Ka�da wsp�pracuj�ca
sie� jest ma uwierzytelniany zapis do listy "czarnych dziur" w celu
zapobiegni�cia nadu�yciom. Dostarczone jest tak�e narz�dzie klienckie.
Poniewa� w proces nie s� zaanga�owani ludzie, RABL dzia�a jako
samodzielny monitor aktywno�ci i mo�e funkcjonowa� samodzielnie. Nie
ma tak�e nikogo do pozwania (poniewa� nie mo�na pozwa� komputer�w za
rozmawianie mi�dzy sob�), co czyni dzia�anie mniej k�opotliwym dla
wsp�pracuj�cych.

%package server
Summary:	Reactive Autonomous Blackhole List server
Summary(pl):	Serwer RABL (reaktywnej autonomicznej listy "czarnych dziur")
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

%description server -l pl
Serwer RABL to cz�� serwerowa czarnych list. Jest wymagana tylko do
u�ywania serwera w�asnej lokalnej RABL. Aby po prostu zapisa� si� do
publicznej RABL potrzebny jest klient RABL.

%package client
Summary:	Reactive Autonomous Blackhole List client
Summary(pl):	Klient RABL (reaktywnej autonomicznej listy "czarnych dziur")
Group:		Applications/Mail

%description client
The RABL client is the lookup and reporting component of the RABL. It
is necessary for performing streaming connection lookups and writing
to the RABL (assuming you have an account).

%description client -l pl
Klient RABL to cz�� RABL s�u��ca do sprawdzania i raportowania. Jest
potrzebny do sprawdzanai po��cze� strumieniowych i zapisu do RABL (w
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
