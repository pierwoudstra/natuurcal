import datetime
import io
import csv
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2_V2
import time
from datetime import date
from PIL import Image,ImageDraw,ImageFont
import traceback

# logging.basicConfig(level=logging.DEBUG)

epd = epd4in2_V2.EPD()
epd.init()
epd.Clear()

font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
font50 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 50)
font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)

def get_message_for_day(day_data):
    """
    Gets the current date and looks up the activity in the provided data.
    """

    now = datetime.datetime.now()
    
    current_day = now.strftime("%d")
    current_month_name = now.strftime("%B")
    

    month_to_num = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    current_month_num = month_to_num.get(current_month_name, '??')

    print(f"--- Today's Date: {current_day} {current_month_name} ({current_month_num}) ---")

    for row in day_data:


        if row['Day'] == current_day and row['Month'] == current_month_num:
            activity = row['Activity'].replace('\n', ' ')
            
            return activity.strip()
            
    print("~~~~")


csv_data = """Day,Month,Activity
01,May,"Female cuckoos \narriving."
02,May,"The first nightjars \narrive, churring and \nwing clapping at \ndusk."
03,May,"Wild bluebells are \nin full flower \nin the woods."
04,May,"Young tawny owls \nmay be calling \nnow, before they \nhave broken out \nof their egg."
05,May,"The first young \ngrebes have hatched \nand are carried \non the backs \nof their parents."
06,May,"Spotted flycatchers are \narriving from Africa."
07,May,"The first golden \norioles can be \nheard."
08,May,"Oaks in flower, \nproducing a lot \nof pollen."
09,May,"Orange tip and \nholly blue butterflies \non wing."
10,May,"The last of \nthe summer migrants \narrive: swifts are \nscreaming across the \nsky."
11,May,"Oxeye daisy in \nflower."
12,May,"Butterflies abound: speckled \nwood, wall brown, \ngreen-veined white, dingy \nskipper on wing."
13,May,"Meadow froghoppers are \nappearing from their \nfoam ‘cuckoo spit’ \nnests."
14,May,"Young moles are \nbeing born."
15,May,"Young eels start \nascending rivers from \nthe sea."
16,May,"Bogbean and yellow \niris in flower \nalong the banks \nof ponds."
17,May,"The air is \nfull of blackbird \nsong."
18,May,"Ash are coming \ninto leaf, one \nof the last \ntrees of the \nspring."
19,May,"Swallowtail butterflies are \non the wing."
20,May,"The first red \ndeer calves of \nthe year are \nbeing born."
21,May,"Young great tits \nare leaving their \nnests."
22,May,"Most swifts have \nlaid an egg \nunder loose roof \ntiles."
23,May,"Mistle thrushes cease \nsinging, their work \ndone."
24,May,"Fox cubs are \nemerging from their \nearths and playing \nabove the ground."
25,May,"Common spotted orchid, \ncommon mallow, yellow \ntattle are in \nflower."
26,May,"Brightly coloured garden \ntiger moths are \non the wing."
27,May,"Hummingbird hawk-moths are \non the wing, \nlooking for nectar."
28,May,"The first caddisflies \nare emerging."
29,May,"Robins have their \nsecond brood; the \nyoung of the \nfirst brood have \nleft their nest."
30,May,"Meadows are full \nof buttercups."
31,May,"Poisonous hound’s tongue \nis in flower."
01,June,"Most Eurasian hobbies \nhave laid an \negg."
02,June,"The flowering period \nof the lesser \nbutterfly orchid begins."
03,June,"Female cuckoos are \nvisiting nests, removing \none of the \neggs to lay \none of their \nown."
04,June,"Wild dog roses \nare blooming."
05,June,"Hedgehogs are giving \nbirth."
06,June,"Extremely poisonous deadly \nnightshade or belladonna \nin flower."
07,June,"Meadowsweet with large \nwhite plumes is \nflowering in damp \nmeadows."
08,June,"Rough chervil is \nin flower."
09,June,"The green tortrix \nmoth is looking \nfor suitable leaves \nto roll them \ninto egg cases."
10,June,"Snipe are displaying \nby flying downwards \nmaking a ‘drumming’ \nnoise with their \nvibrating tail feathers."
11,June,"Most of the \nfemale reed warblers \nhave laid their \neggs."
12,June,"Poppies are flowering \nin fields, on \nunused sites and \nroad sides."
13,June,"Stag beetles are \nemerging."
14,June,"Young swallows are \nbig enough to \nstart leaving their \nnests."
15,June,"The first edible \ngiant puffballs are \nappearing in meadows."
16,June,"Large and small \ntortoiseshell butterflies can \nbe seen."
17,June,"Bats are fully \nactive, each catching \nthousands of insects \nat night."
18,May,"Scotch bonnet fungi \nsuddenly appear in \npastures and sometimes \nin fairy-rings."
19,June,"Young harvest mice \nare in their \nwoven grass nests \nsuspended between stalks."
20,June,"Blackbirds stop brooding \nand stop their \npassionate singing."
21,June,"The first young \ntoads are moving \nonto dry land."
22,June,"Small skipper butterflies \nare on the \nwing."
23,June,"Common seals are \ngiving birth to \ntheir young on \nsand flats in \nthe sea."
24,June,"Great horse-flies \nare emerging."
25,June,"The cuckoo gradually \nstops calling its \nown name."
26,June,"The dark green \nfritillary is on \nthe wing with \nits black-orange chequered \nwings."
27,June,"Chaffinches cease singing."
28,June,"Harbour porpoises concentrate \non breeding; their \nyoung are born \neleven months later."
29,June,"Grass snakes are \nlaying their eggs \nin sweltering dung \nhills and compost \nheaps."
30,June,"Elephant hawk-moths are \nvisiting honeysuckle flowers \nfor pollination."
01,July,"Glowworms are emerging."
02,July,"The first wasps \nstart looking for \nsomething sweet for \ntheir young."
03,July,"Rosebay willowherb is \nflowering."
04,July,"Vervain is flowering."
05,July,"Brown hawker dragonfly \nand willow emerald \ndamselfly are on \nthe wing."
06,July,"Female bats are \nsuckling their young."
07,July,"Most of the \nadult cuckoos have \ndeparted to Africa."
08,July,"Purple emperor butterflies \non wing near \nwillows."
09,July,"Young magpies are \nfollowing their parents, \nbegging them for \nfood."
10,July,"Roe deer start \nmating."
11,July,"Silver-washed fritillary butterflies \nappear."
12,July,"Sundews are flowering \nin sphagnum bogs."
13,July,"The red berries \nof the rowans \nare ripening."
14,July,"Largest number of \ncommon blue damselflies \nare on the \nwing."
15,July,"In sunny places \nthe first blackberries \nare ripe."
16,July,"Female otters are \ngiving birth."
17,July,"Cotton grasses and \nbog asphodel are \nflowering."
18,July,"Meadow brown butterfly, \ndark green fritillary \nand large blue \nare on the \nwing."
19,July,"Song thrushes cease \nsinging."
20,July,"Rose bedeguar galls \nare appearing on \nwild rose species."
21,July,"The first chantarelle \nfunguses are appearing \nin beech woods."
22,July,"Most birdsong has \nended but skylarks \nand yellowhammers are \nstill singing."
23,July,"Wasps on the \nwing abound."
24,July,"The large copper \ncan be spotted \nflying."
25,July,"Clouded yellow butterflies \nare appearing on \nclover and alfalfa \nfields."
26,July,"Common seals begin \ntheir display and \nmating ritual."
27,July,"Migrant hawker dragonflies \nare on the \nwing."
28,July,"Small skipper butterflies \nare on the \nwing."
29,July,"Water dropwort is \nflowering. Its roots \nare very poisonous."
30,July,"Honeysuckle berries start \nripening."
31,July,"Gipsywort or bugleweed \nis in bloom \nin wetland areas."
01,August,"Second broods of \nswallows are fledging."
02,August,"Caterpillars of the \neyed hawk-moth \nfully fed."
03,August,"Small red-eyed damselfly \non wing."
04,August,"The common earthball \nfungus attacked by \nthe parasitical Boletus \nparasiticus."
05,August,"Ivy-leaved bellflower in \nflower."
06,August,"Foxgloves are abundant."
07,August,"Yellowhammers stop singing."
08,August,"Young frogs have \ndispersed and forage \nfor insects in \nthe grass."
09,August,"Devil’s-bit scabious still \nin flower."
10,August,"Swifts begin to \nleave for Africa."
11,August,"Small tortoiseshell butterfly \non wing."
12,August,"Young slowworms hatch."
13,August,"Second broods of \nmartins fledged."
14,August,"Robins commence their \nautumn song."
15,August,"Moles cast out \ntheir young."
16,August,"Blue hawker dragonfly \non wing."
17,August,"Small emerald spreadwing \non wing."
18,August,"Great woolly-headed thistle \nflowering."
19,August,"Larvae of elephant \nand privet hawk-moths \nalmost fully fed."
20,August,"The fungus Amanita \nmappa appears on \nsandy soil under \noaks and beeches."
21,August,"Young bats begin \nto catch insects \nfor themselves and \nno longer need \ntheir mothers’ milk."
22,August,"Smooth snakes are \ngiving birth to \nlive young."
23,August,"Winged ants appear \nin swarms from \nants’ nests."
24,August,"Lapwings flock together \nfor their autumnal \nmigration."
25,August,"Flying alone and \nfor the first \ntime, young cuckoos \nare departing for \nAfrica."
26,August,"Horn of plenty \nor “trumpet of \ndeath” fungus is \nappearing in woods."
27,August,"The adonis blue \nbutterfly is on \nthe wing."
28,August,"Caterpillars of the \nemperor moth are \nfeeding on heather."
29,August,"Adult shrews are \nat the end \nof their lives \nand die of \nexhaustion."
30,August,"The first elder \nberries are ripe \nand are eaten \nby wood pigeons."
31,August,"Peacock butterflies can \nbe found on \nthe wing or \nresting."
01,September,"Death’s-head hawkmoths are \non the wing."
02,September,"Many glistening inky \ncap fungi can \nbe found."
03,September,"Blackberries start ripening."
04,September,"Young natterjack toads \nare leaving the \nwater."
05,September,"Silk-button spangle galls \nare appearing on \nthe back of \noak leaves."
06,September,"Fancifully shaped knopper \ngalls are falling \nfrom oaks."
07,September,"The last silver-spotted \nskippers can be \nspotted on the \nwing."
08,September,"Wasp nest beetles \nappear from underground \nwasps’ nests."
09,September,"Parasol fungi appear \nin meadows and \nalong road sides."
10,September,"Crane flies or \ndaddy longlegs are \nabundant."
11,September,"The first horse \nchestnuts are ripe \nand fall from \nthe trees."
12,September,"Shaggy ink cap \nfungus appears on \ndisturbed and nutrition-rich \nsoils."
13,September,"The stemless dwarf \nthistle can still \nbe found blooming."
14,September,"Lime trees begin \nto shed their \nleaves."
15,September,"Red deer stags \nstart their mating \nseason rutting."
16,September,"Common kingfishers can \nbe spotted frequently."
17,September,"The first acorns \nare falling."
18,September,"Bracken assumes its \nautumnal tinting."
19,September,"Male badgers are \npreparing their burrows \nto accommodate multiple \nfemales."
20,September,"The first barn \nswallows and martins \nstart their migration \nsouth."
21,September,"Beech-nuts are now \nplentiful in the \nwoods."
22,September,"Ivy is beginning \nto bloom."
23,September,"Mistle thrushes are \nfeeding on ripe \norange rowan berries."
24,September,"Caddis fly are \nswarming over ponds \nin the evening."
25,September,"Turtle doves are \nleaving to spend \nthe winter in \nWest Africa."
26,September,"Second flowering of \nhoneysuckle."
27,September,"False truffles can \nbe seen in \npine woods, after \nrabbits have dug \nthem up."
28,September,"Dormice and squirrels \nare stocking up \ntheir winter supplies."
29,September,"Scarlet waxcap fungi \nare appearing in \nfields and on \nlawns."
30,September,"Migrating silver Y \nmoths are on \ntheir way south."
01,October,"Adult eels are \nmigrating from inland \nwaters to the \nsea on their \nway to their \nspawning grounds in \nthe Sargasso Sea."
02,October,"Many trees, including \nbeeches, are changing \ncolour to autumn \ntints."
03,October,"Hips, haws and \nsloes are now \nripe."
04,October,"Field mushrooms in \nstriking fairy-rings are \nin fields and \non lawns."
05,October,"Rutting red deer \nare using their \nantlers in the \ncompetition for hinds."
06,October,"Fly agaric are \nemerging under birches \nand other trees."
07,October,"Starlings are starting \nto roost in \nhuge flocks."
08,October,"The last flights \nof the green-veined \nwhite butterfly before \nit hibernates as \na pupa."
09,October,"Queen wasps are \ngoing into hibernation."
10,October,"Blackbirds are feeding \non fallen apples."
11,October,"Ladybird beetles are \ngoing into hibernation, \noften in homes."
12,October,"The trees are \nshedding their leaves \nbut oak and \nash trees are \nstill very green."
13,October,"Cauliflower fungus is \nappearing at the \nbase of Scots \npine trunks."
14,October,"Chaffinches and lesser \nredpolls are sometimes \nsinging on fine \nmornings."
15,October,"Wrens are beginning \ntheir autumn singing."
16,October,"The last martins \nand barn swallows \nare leaving to \nspend the winter \nin Africa."
17,October,"Dogwood leaves are \nturning a beautiful \nred."
18,October,"At dusk blackbirds \nare making their \nshort high pitch \nalarm calls."
19,October,"Some young wood \npigeons are leaving \nthe nest only \nnow."
20,October,"Amphibians start withdrawing \ninto their hibernation \nshelters."
21,October,"The vomiting russula \nor the sickener \nfungus is appearing \non damp, acid \nsoils."
22,October,"The northern red \noak takes on \na striking red."
23,October,"The first fieldfares \nare arriving from \nthe high north."
24,October,"Brent geese are \nreturning from their \nnorthern breeding grounds \nwith their young."
25,October,"Slowworms are going \ninto hibernation, hidden \nin humus and \nrough grasses."
26,October,"The first woodcocks \nare arriving from \nFinland and Russia \nto spend the \nwinter here."
27,October,"Comma butterflies have \nstopped flying for \nthis year."
28,October,"The birch leaves \nhave taken on \ntheir autumnal colours."
29,October,"Peacock butterflies stop \nflying as autumn \nprogresses."
30,October,"Dormice are going \ninto hibernation until \nApril."
31,October,"Virtually all butterflies \nhave stopped flying \nbecause of the \ncold."
01,November,"Mistle thrushes begin \nsinging again from \ntreetops."
02,November,"The brown long-eared \nbat starts to \nhibernate in trees, \nhollow walls, caves \nand mines."
03,November,"The grass stops \ngrowing."
04,November,"Money spiders in \nvast numbers on \nfields cover the \ngrass with threads \nof silk."
05,November,"Autumnal leaf tinting \nis usually at \nits best about \nthis time."
06,November,"Mermaids purses holding \nshark’s or skate’s \neggs, wash up \non beaches."
07,November,"Serotine bats are \nspending the winter \nin cavity walls, \nunder roof tiles \nand in disused \nchimneys."
08,November,"Salmon start to \nascend rivers from \nthe sea to \nspawn upstream."
09,November,"The last red \nadmiral butterflies are \nstill on wing."
10,November,"Thousands of wild \ngeese are back \nfrom their summer \nbreeding grounds in \nthe Arctic."
11,November,"Adult shrews die \nof exhaustion, the \nyoung are left \nto survive the \nwinter."
12,November,"Frogs hibernate in \nthe unfrozen muddy \nlayer on the \nbottom of ponds \nand pools."
13,November,"Candlesnuff fungus is \nabundant on old \nstumps."
14,November,"The colourful butter \nwaxcap appears in \nmeadows."
15,November,"The spitting spider \nScytodes thoracica goes \nhunting by night."
16,November,"Adders and grass \nsnakes go into \nhibernation."
17,November,"Hedgehogs go into \nhibernation until April."
18,November,"Lapwings are feeding \nin flocks on \nfields."
19,November,"Brown witch’s butter \nfungus or jelly \nleaf is growing \non dead birch \nand oak branches."
20,November,"Occasional appearance of \nbrimstone butterflies."
21,November,"Squirrels retire to \ntheir winter retreats."
22,November,"Most moths start \nto hibernate as \na pupa among \nfallen leaves or \nother hidden spots."
23,November,"Long-eared owls form \ncommunal roosts."
24,November,"Greenfinches assemble in \nflocks for their \ncollective wintering."
25,November,"Common bracket fungus \nis abundant on \ndead wood."
26,November,"The pedunculate or \nEnglish oaks are \nnow completely bare."
27,November,"The nettle cells \nof stinging-nettles are \nlosing strength."
28,November,"The Fluted bird’s \nnest fungus ejects \nits spores."
28,November,"Young magpies without \na territory are \nroosting in small \nflocks."
30,November,"Pipistrelle bats are \ngoing into hibernation."
01,December,"Today the meteorological \nwinter begins."
02,December,"The common shrew \nis now underground \nand hunting for \ninvertebrates."
03,December,"Male foxes are \ncalling in the \nnight to find \na female to \nmate with."
04,December,"Nathusius’ pipistrelle bats \nmay fly on \nmild winter days."
05,December,"Red-stemmed feather moss \nabundant on sandy \nsoil."
06,December,"The rough-mantled doris \nsea slug is \nlooking for barnacles \nto feed on \nduring its breeding \ntime."
07,December,"Yellowhammers are congregating \nin winter flocks \nat nutrition-rich \nplaces."
08,December,"At night luminous \ncentipedes can be \nspotted."
09,December,"The first young \nof grey seals \nare being born."
10,December,"Blackbirds clear circles \nof dead leaves \nto get at \ninsects and worms \nin the ground."
11,December,"The song thrush \nsings at dawn \nin mild weather."
12,December,"Titmice extract larvae \nfrom oak marble \ngalls and eat \nthem."
13,December,"Groundsel can be \nseen in flower, \nin sheltered places \nall year long."
14,December,"Stoats have their \nwhite coat for \nwinter."
15,December,"The mating season \nof squirrels has \nbegun."
16,December,"The high, sharp \ncall of the \ngreat spotted woodpecker \ncan be heard \nhigh up in \nthe trees."
17,December,"Shepherd’s purse is \noccasionally still flowering."
18,December,"Many insects winter \nin the hollow \nstems of dead \nplants."
19,December,"The first scarlet \nelf cup fungi \nappear."
20,December,"Long-tailed tit flocks \nare looking for \nfood all day \nto survive."
21,December,"Common chickweed is \noccasionally still flowering."
22,December,"Compass jellyfish come \nnear to the \nshore."
23,December,"Slowworms can be \nspotted in sunny \nweather."
24,December,"Early nuthatches commence \ntheir spring whistle."
25,December,"Stag beetles can \nbe spotted on \na clear evening."
26,December,"Yellow witch’s - \nbutter fungus can \nbe seen on \nthe stems of \ndead oak and \nother trees."
27,December,"Yellow gorse is \nflowering profusely."
28,December,"Moles throw up \nhillocks when the \nground is not \nfrozen hard."
29,December,"Robins are singing."
30,December,"Wild boars churn \nup the fallen \nleaves looking for \nacorns."
31,December,"Earthworms tug/pull dead \nleaves into their \nholes and eat \nthem."
01,January,"Badgers are asleep \ndeep underground."
02,January,"Dunnocks commence their \nbirdsong."
03,January,"The black-spotted chestnut \nmoth can be \nspotted flying in \nthe night."
04,January,"Marsh tits begins \nto sing."
05,January,"Beavers are satisfying \ntheir appetite with \nwillow bark."
06,January,"Rabbits gnaw the \nbark of holly \nand other scrubs \nif the weather \nis severe."
07,January,"Stock doves can \nbe heard calling."
08,January,"Smooth newts begin \nbreeding if the \nweather is warm \nenough."
09,January,"Rabbits start devoting \nthemselves to breeding."
10,January,"Lesser spotted woodpecker \nsometimes drums."
11,January,"Red dead-nettle already \nflowering here and \nthere."
12,January,"The pale brindled \nbeauty moth flies \nfrom now till \nlate April."
13,January,"Swan’s-neck thread moss \nis forming its \nreproductive organs."
14,January,"Common winter damselflies \non wing on \nwarm days."
15,January,"First yellow daffodils \nare flowering."
16,January,"The first buntings \nstart singing."
17,January,"Dark green cushions \nof broom fork-moss \nare growing on \nsandy banks and \ntree trunks."
18,January,"The loudest singers \nnow are the \ngreat tits."
19,January,"Brown hairstreak butterflies \nare laying eggs \nin blackthorn bushes."
20,January,"Beavers are starting \ntheir mating season."
21,January,"Wood larks are \nsinging."
22,January,"Black witch’s butter \nfungus (Exidia glandulosa) \nis growing on \ndead branches."
23,January,"Dumbledore beetle appears."
24,January,"First snowdrop leaves \nare emerging from \nthe snow."
25,January,"Early skylarks start \nsinging."
26,January,"Nathusius’ pipistrelle bats \nmay be spotted \nflying if it \nis not too \ncold."
27,January,"Hare mating season \nbegins and continues \nwell into summer."
28,January,"The first robins \nstart building their \nnests."
29,January,"Winter gnats abound."
30,January,"The first snowdrops \nbegin to flower."
31,January,"Earthworms lie out."
01,February,"Small tortoiseshell butterflies \nstart to emerge \nfrom hibernation."
02,February,"Greenfinches separate from \nflocks to continue \non their own."
03,February,"Moles prepare their \nunderground nests for \ntheir young."
04,February,"Tree creepers commence \ntheir spring call."
05,February,"Tawny owls hoot \nat dusk."
06,February,"Hawfinches feed on \nholly berries."
07,February,"Blackbirds sing at \ndusk."
08,February,"Winter jasmine is \nflowering profusely."
09,February,"Collared doves are \ncooing loudly in \nthe morning."
10,February,"First crop of \nglistening ink cap \nfungus appears on \ndead broad-leaved \ntrees."
11,February,"Greater spotted woodpeckers \ndrum to mark \ntheir territory."
12,February,"Male moles in \nsearch for a \npartner dig long \ntunnels throwing up \nmany hillocks."
13,February,"Badgers are giving \nbirth to young."
14,February,"Woodcocks are making \ntheir flight displays \n‘roding’, to mark \ntheir breeding territory."
15,February,"Yellowhammer starts to \nsing its characteristically \nshrill notes."
16,February,"Barn owls are \nmating."
17,February,"Peacock and brimstone \nbutterflies emerge from \nhibernation."
18,February,"First primroses appearing."
19,February,"The great crested \ngrebe’s mirror courtship \ndance begins."
20,February,"Salmon start to \ndescend rivers on \ntheir migration to \nthe sea."
21,February,"Frogs are busy \nmating and producing \nfrogspawn."
22,February,"Chaffinches commence singing."
23,February,"Lesser periwinkle blooming \nwith brightly blue \nflowers."
24,February,"Goldcrests begin their \nalmost inaudibly high \nchirping."
25,February,"Adders emerge from \nhibernation."
26,February,"Brent geese start \nto leave for \nthe Arctic islands."
27,February,"Early-nesting herons already \nhave eggs."
28,February,"Slowworms revive from \ntorpidity."
01,March,"Most tawny owls \nhave laid their \neggs."
02,March,"Wood anemones in \nflower in woodland."
03,March,"The first queen \nwasps emerge from \nhibernation."
04,March,"Willows and marsh-marigolds \nin flower."
05,March,"Curlews begin their \ndisplay flights, rising \nsteeply then gliding \ndown while singing."
06,March,"Mistle thrushes are \nnesting."
07,March,"Blackthorn in flower."
08,March,"Early swans may \nstart building their \nnest."
09,March,"First lesser celandine \nflowers appearing."
10,March,"Male hares start \nto fight, standing \non hind legs \nand boxing."
11,March,"The first generation \nof brimstone butterflies \nstart their flight \nperiod."
12,March,"Male yews begin \nshedding abundant amounts \npollen."
13,March,"The large white \nbutterflies are on \nthe wing."
14,March,"Sparrowhawks can be \nseen soaring over \ntheir territories only \nat this time \nof year."
15,March,"Common frogs start \nto emerge."
16,March,"Black ants remove \nthe seal from \nthe entrance to \nthe nest and \nbegin to forage \nabove ground."
17,March,"The first speckled \nwood butterflies can \nbe spotted flying."
18,March,"Common frogs start \ncroaking to attract \nthe attention of \nfemales."
19,March,"Wrens are singing \nhigher in the \ntrees, their voices \ncarrying further."
20,March,"The first young \nEuropean pine martens \nare born."
21,March,"The first newts \nreturn to the \nwater."
22,March,"Rosemary has started \nflowering."
23,March,"First horse chestnut \nleaves are unfolding."
24,March,"Toads are mating \nand laying eggs."
25,March,"Kingfishers are looking \nfor nesting holes."
26,March,"First hazel leaves \nare appearing."
28,March,"Magnolia flowering before \nthe first leaves \nappear."
22,March,"Wheatears have arrived, \none of the \nfirst long-distance migrant \nbirds to return."
30,March,"Long-eared owls are \nnesting."
31,March,"Crows, jackdaws, magpies \nand rooks are \nbuilding or repairing \ntheir nests."
01,April,"Mating season has \nstarted for adders; \nthe males compete \nin a dance/fight \nto impress females."
02,April,"The first Chiffchaffs \nhave returned and \nbegin to sing \ntheir name."
03,April,"The first young \nof the wild \nboar are born."
04,April,"First willow warbler \nsong can be \nheard."
05,April,"Tadpoles abound in \nponds and pools."
06,April,"Sparrowhawks and kestrels \nnesting."
07,April,"The first nightingale \nreturns."
08,April,"Most buzzards have \nlaid their first \negg."
09,April,"The distinctive orange-tip \nbutterflies are flying."
10,April,"Grass snakes are \nmating."
11,April,"Cuckoo males begin \nto arrive from \nSub-Saharan Africa and \nstart calling their \nname."
12,April,"Beavers are having \ntheir first young."
13,April,"Ash trees are \nflowering."
14,April,"Yellow wagtails have \narrived from their \nwinter retreats."
15,April,"Hedgehogs are emerging \nfrom hibernation."
16,April,"Small tortoiseshell butterfly \nand comma butterfly \nare at the \npeak of their \nflight period."
17,April,"Young mallards are \nhatching and can \nbe seen swimming."
18,April,"Crab apples flowering."
19,April,"Grey squirrels prepare \ntheir dreys (tree \nnests)."
20,April,"Yellow archangel in \nflower."
21,April,"Sandpipers, European pied \nflycatchers, grasshopper warblers \nand many other \nbirds have returned \nto the country."
22,April,"Pedunculate or English \noak leaves unfolding."
23,April,"Hawthorn starts flowering."
24,April,"The wood warbler \nhas arrived to \nspend the summer."
25,April,"Great and blue \ntits are now \nsitting on eggs."
26,April,"Rare migrating turtle \ndoves that have \nsurvived being hunted \nwhile crossing Malta \narrive in UK."
27,April,"First flowers of \nthe horse chestnut \ntree appearing."
22,April,"The reed warbler \nis in the \ncountry."
29,April,"The first swift \nhas arrived and \nwill stay for \none hundred days."
30,April,"The male wren \nis busy making \nseveral nests, the \nfemale chooses one \nof them."""

csv_file = io.StringIO(csv_data)

data_reader = csv.DictReader(csv_file)
data_with_numbers = []

month_to_num = {
    'January': '01', 'February': '02', 'March': '03', 'April': '04',
    'May': '05', 'June': '06', 'July': '07', 'August': '08',
    'September': '09', 'October': '10', 'November': '11', 'December': '12'
}

for row in data_reader:
    month_name = row['Month']
    row['Month'] = month_to_num.get(month_name)
    
    if row['Month'] is not None:
        row['Day'] = row['Day'].zfill(2)
        data_with_numbers.append(row)


if __name__ == "__main__":
    print(get_message_for_day(data_with_numbers))
    while(True):
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.rectangle((140, 80, 240, 105), fill = 255)
        draw.text((20, 10), time.strftime('%H:%M:%S'), font = font50, fill = 0)
        draw.text((20,60), date.today().strftime("%A %d. %B %Y"), font = font18, fill = 0)
        draw.text((1, 200), get_message_for_day(data_with_numbers), font = font18, fill = 0)
        epd.display_Partial(epd.getbuffer(Himage))