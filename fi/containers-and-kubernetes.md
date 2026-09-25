# Kontit — asetukset

## Mitä vaaditaan

Vain ohjelman `docker` tai `kubectl` on oltava tavoitettavissa koneella, joka suorittaa työn. Mitään muuta ei tarvita. Docker Desktop ei ole vaatimus. Docker Engine Linuxissa, Rancher Desktop, Colima ja Podman Docker-yhteensopivalla komennolla toimivat kaikki samalla tavalla, koska sovellus yksinkertaisesti suorittaa komennon, jonka se löytää järjestelmäpolulta.

Kubernetes toimii samoin. Kaikki `kubectl`:n kautta tavoitettavissa olevat klusterit ovat tuettuja, mukaan lukien k3s, kind, minikube ja hallitut klusterit, kuten EKS, GKE tai AKS.

## Toisen demonin tai klusterin käyttäminen

Jos haluat lähettää töitä toiselle Docker-daemonille, aseta `DOCKER_HOST` tai vaihda komennolla `docker context use`. Jos haluat käyttää toista Kubernetes-klusteria, vaihda nykyistä kontekstia `kubectl config use-context`:lla. Sovellus seuraa mitä tahansa komentorivin jo käyttämää, joten lisäasetuksia ei tarvita sovelluksen sisällä.

## Missä tiedostot on asennettu

Kubernetesille kansio liitetään kahdella tavalla. Paikalliset kehityskontekstit saavat suoran isäntäkansioasennuksen. Se kattaa kontekstin nimeltä `desktop`, `colima` tai `orbstack`, kontekstin, jonka nimi päättyy merkkijonoon `@desktop`, kontekstin, jonka nimi alkaa merkkijonolla `kind-`, `minikube` tai `k3d-`, sekä kontekstin, jonka nimi sisältää merkkijonon `docker-desktop`, `docker-for-desktop` tai `rancher-desktop`. Jokaista muuta kontekstia käsitellään todellisena klusterina ja se saa sen sijaan jatkuvan taltiovaatimuksen, koska todellinen klusterin solmu ei näe työpöytäkoneen kansioita. Kun `ORGANIZE_FILES_K8S_VOLUME_MODE` asetetaan arvoon `pvc` tai `hostpath`, se ohittaa tämän valinnan kaikissa konteksteissa.

## Verkkokansiot Windowsissa

Docker Desktop Windowsissa ei voi liittää verkkopolkua, kuten `\\server\share`, Linux-säilöyn. Windows näkee kansion, mutta säilö ei. Sen kiertämiseen on kaksi tapaa. Käytä paikallisella levyllä olevaa kansiota tai suorita työ sen sijaan sovelluskohteella, joka tekee työn itse sovelluksessa. Jakoon yhdistetty asemakirjain ei auta, koska sovellus seuraa sen takaisin verkkopolkuun ja hylkää sen samalla tavalla.

## Valmiit tiedostot

Linux-komentoripaketeissa on valmiit tiedostot `containers`-kansiossa: Dockerfile, joka rakentaa levykuvan itse paketista, Compose-esimerkki, Kubernetesin Job-esimerkit sekä `containers/README.md` ja sen vieressä README jokaiselle kielelle.

# Kontit ja CLI-workerit

## Suunnitellut työt — Docker- ja Kubernetes-kohteet

Avaa **Työt** pääikkunan sivupalkista. Napsauta **Uusi tehtävä** tai **Muokkaa** olemassa olevassa kortissa. Valitse avattavasta **Kohde**-valikosta **Docker-komento** tai **Kubernetes-työ**.

1. Aseta **Lähteet** (isäntäpolut) ja **Tuloste** (isäntäpolku – täytyy olla olemassa jo ennen työn suorittamista).
2. Valitse **Tila** ja **Suorita asetukset** kuten muillekin töille.
3. **Komennon esikatselu** -paneeli näyttää tarkan käytettävän Docker run -komennon tai Kubernetes Job YAML:n.
4. **Tallenna** työ ja aseta **Aikataulu** tai aloita heti napsauttamalla kortissa **Suorita nyt**.

Sovellus luo asennusliput ja volyymipolut automaattisesti tallennetusta tilannekuvasta. Docker-daemonin tai "kubectlin" on oltava tavoitettavissa isäntäkoneella. **Preflight** tarkistaa liitettävyyden ja raportoi kaikki virheet työlokissa ennen ajon alkamista. Katso hyväksyntäkulku, lokien haku ja headless-ajoitus kohdasta **Ajoitetut työt**.

## Isäntäkoneen pääte (PowerShell / bash / cmd)

Kyllä — isäntäkoneella suorita **OrganizeFiles.Cli** PowerShellistä, bashista tai cmd:stä. Se on tuettu päätereitti. Avalonian työpöytäikkuna on erillinen graafinen käyttöliittymä. Julkaise tai asenna CLI-paketti sovelluksen viereen (tai PATH-polkuun) ja anna sitten **--source** (toistettavissa), **--output** ja **--mode**. Aloita mieluiten testiajolla. Lisää **--execute** vasta kun olet valmis.

## Työpöydän käyttöliittymä ja säiliöt

Kontit ja automaatio: Avalonia-työpöytäkäyttöliittymää ei ole tarkoitettu toimimaan tyypillisessä headless-Linux-säiliössä. Käytä OrganizeFiles.Cli-paria yhdelle tai useammalle erilliselle työlle, mukaan lukien useita rinnakkaisia työntekijöitä: liitä jokaiseen säilöön lähdekansiot vain luku -tilassa testiajon esikatselutöitä varten. Todelliset siirrot komennolla **--execute** vaativat kirjoitettavan lähdekiinnitteen, koska moottori siirtää tiedostot pois lähdepuusta. Käytä erillistä luku-/kirjoitustulostelevyä, varmista kelvollinen tallennuksen tai julkaisijan käyttöoikeus kaikille järjestämis-/korjausajoille (testiajo ja suoritus), anna **--source** (toistettavissa), **--output** ja **--mode**. Jokainen samanaikainen työntekijä tarvitsee oman lähtöjuuren. Kansion **Tuloste** on oltava jo olemassa isännässä ennen kuin Docker- tai Kubernetes-työt suoritetaan (preflight hylkää puuttuvan kohteen eikä luo sitä). Esimerkkipolut: containers/README.md ja containers/docker-compose.sample.yml. Jobs/JobAgent luotu `docker run` liittää lähteet kohtaan `/in1`, `/in2`, … ja ulostulon kohtaan `/out`. Manuaalisissa yhden lähteen esimerkeissä voidaan käyttää `/in` (katso containers/README.md).
