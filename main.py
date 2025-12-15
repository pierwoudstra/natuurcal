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

    # print(f"--- Today's Date: {current_day} {current_month_name} ({current_month_num}) ---")

    for row in day_data:


        if row['Day'] == current_day and row['Month'] == current_month_num:
            activity = row['Activity']
            
            return activity.strip()
            
    print("~~~~")


csv_data = """Day,Month,Activity
01,May,"Female cuckoos \n arriving."
02,May,"The first nightjars \n arrive, churring and \n wing clapping at \n dusk."
03,May,"Wild bluebells are \n in full flower \n in the woods."
04,May,"Young tawny owls \n may be calling \n now, before they \n have broken out \n of their egg."
05,May,"The first young \n grebes have hatched \n and are carried \n on the backs \n of their parents."
06,May,"Spotted flycatchers are \n arriving from Africa."
07,May,"The first golden \n orioles can be \n heard."
08,May,"Oaks in flower, \n producing a lot \n of pollen."
09,May,"Orange tip and \n holly blue butterflies \n on wing."
10,May,"The last of \n the summer migrants \n arrive: swifts are \n screaming across the \n sky."
11,May,"Oxeye daisy in \n flower."
12,May,"Butterflies abound: speckled \n wood, wall brown, \n green-veined white, dingy \n skipper on wing."
13,May,"Meadow froghoppers are \n appearing from their \n foam ‘cuckoo spit’ \n nests."
14,May,"Young moles are \n being born."
15,May,"Young eels start \n ascending rivers from \n the sea."
16,May,"Bogbean and yellow \n iris in flower \n along the banks \n of ponds."
17,May,"The air is \n full of blackbird \n song."
18,May,"Ash are coming \n into leaf, one \n of the last \n trees of the \n spring."
19,May,"Swallowtail butterflies are \n on the wing."
20,May,"The first red \n deer calves of \n the year are \n being born."
21,May,"Young great tits \n are leaving their \n nests."
22,May,"Most swifts have \n laid an egg \n under loose roof \n tiles."
23,May,"Mistle thrushes cease \n singing, their work \n done."
24,May,"Fox cubs are \n emerging from their \n earths and playing \n above the ground."
25,May,"Common spotted orchid, \n common mallow, yellow \n tattle are in \n flower."
26,May,"Brightly coloured garden \n tiger moths are \n on the wing."
27,May,"Hummingbird hawk-moths are \n on the wing, \n looking for nectar."
28,May,"The first caddisflies \n are emerging."
29,May,"Robins have their \n second brood; the \n young of the \n first brood have \n left their nest."
30,May,"Meadows are full \n of buttercups."
31,May,"Poisonous hound’s tongue \n is in flower."
01,June,"Most Eurasian hobbies \n have laid an \n egg."
02,June,"The flowering period \n of the lesser \n butterfly orchid begins."
03,June,"Female cuckoos are \n visiting nests, removing \n one of the \n eggs to lay \n one of their \n own."
04,June,"Wild dog roses \n are blooming."
05,June,"Hedgehogs are giving \n birth."
06,June,"Extremely poisonous deadly \n nightshade or belladonna \n in flower."
07,June,"Meadowsweet with large \n white plumes is \n flowering in damp \n meadows."
08,June,"Rough chervil is \n in flower."
09,June,"The green tortrix \n moth is looking \n for suitable leaves \n to roll them \n into egg cases."
10,June,"Snipe are displaying \n by flying downwards \n making a ‘drumming’ \n noise with their \n vibrating tail feathers."
11,June,"Most of the \n female reed warblers \n have laid their \n eggs."
12,June,"Poppies are flowering \n in fields, on \n unused sites and \n road sides."
13,June,"Stag beetles are \n emerging."
14,June,"Young swallows are \n big enough to \n start leaving their \n nests."
15,June,"The first edible \n giant puffballs are \n appearing in meadows."
16,June,"Large and small \n tortoiseshell butterflies can \n be seen."
17,June,"Bats are fully \n active, each catching \n thousands of insects \n at night."
18,May,"Scotch bonnet fungi \n suddenly appear in \n pastures and sometimes \n in fairy-rings."
19,June,"Young harvest mice \n are in their \n woven grass nests \n suspended between stalks."
20,June,"Blackbirds stop brooding \n and stop their \n passionate singing."
21,June,"The first young \n toads are moving \n onto dry land."
22,June,"Small skipper butterflies \n are on the \n wing."
23,June,"Common seals are \n giving birth to \n their young on \n sand flats in \n the sea."
24,June,"Great horse-flies \n are emerging."
25,June,"The cuckoo gradually \n stops calling its \n own name."
26,June,"The dark green \n fritillary is on \n the wing with \n its black-orange chequered \n wings."
27,June,"Chaffinches cease singing."
28,June,"Harbour porpoises concentrate \n on breeding; their \n young are born \n eleven months later."
29,June,"Grass snakes are \n laying their eggs \n in sweltering dung \n hills and compost \n heaps."
30,June,"Elephant hawk-moths are \n visiting honeysuckle flowers \n for pollination."
01,July,"Glowworms are emerging."
02,July,"The first wasps \n start looking for \n something sweet for \n their young."
03,July,"Rosebay willowherb is \n flowering."
04,July,"Vervain is flowering."
05,July,"Brown hawker dragonfly \n and willow emerald \n damselfly are on \n the wing."
06,July,"Female bats are \n suckling their young."
07,July,"Most of the \n adult cuckoos have \n departed to Africa."
08,July,"Purple emperor butterflies \n on wing near \n willows."
09,July,"Young magpies are \n following their parents, \n begging them for \n food."
10,July,"Roe deer start \n mating."
11,July,"Silver-washed fritillary butterflies \n appear."
12,July,"Sundews are flowering \n in sphagnum bogs."
13,July,"The red berries \n of the rowans \n are ripening."
14,July,"Largest number of \n common blue damselflies \n are on the \n wing."
15,July,"In sunny places \n the first blackberries \n are ripe."
16,July,"Female otters are \n giving birth."
17,July,"Cotton grasses and \n bog asphodel are \n flowering."
18,July,"Meadow brown butterfly, \n dark green fritillary \n and large blue \n are on the \n wing."
19,July,"Song thrushes cease \n singing."
20,July,"Rose bedeguar galls \n are appearing on \n wild rose species."
21,July,"The first chantarelle \n funguses are appearing \n in beech woods."
22,July,"Most birdsong has \n ended but skylarks \n and yellowhammers are \n still singing."
23,July,"Wasps on the \n wing abound."
24,July,"The large copper \n can be spotted \n flying."
25,July,"Clouded yellow butterflies \n are appearing on \n clover and alfalfa \n fields."
26,July,"Common seals begin \n their display and \n mating ritual."
27,July,"Migrant hawker dragonflies \n are on the \n wing."
28,July,"Small skipper butterflies \n are on the \n wing."
29,July,"Water dropwort is \n flowering. Its roots \n are very poisonous."
30,July,"Honeysuckle berries start \n ripening."
31,July,"Gipsywort or bugleweed \n is in bloom \n in wetland areas."
01,August,"Second broods of \n swallows are fledging."
02,August,"Caterpillars of the \n eyed hawk-moth \n fully fed."
03,August,"Small red-eyed damselfly \n on wing."
04,August,"The common earthball \n fungus attacked by \n the parasitical Boletus \n parasiticus."
05,August,"Ivy-leaved bellflower in \n flower."
06,August,"Foxgloves are abundant."
07,August,"Yellowhammers stop singing."
08,August,"Young frogs have \n dispersed and forage \n for insects in \n the grass."
09,August,"Devil’s-bit scabious still \n in flower."
10,August,"Swifts begin to \n leave for Africa."
11,August,"Small tortoiseshell butterfly \n on wing."
12,August,"Young slowworms hatch."
13,August,"Second broods of \n martins fledged."
14,August,"Robins commence their \n autumn song."
15,August,"Moles cast out \n their young."
16,August,"Blue hawker dragonfly \n on wing."
17,August,"Small emerald spreadwing \n on wing."
18,August,"Great woolly-headed thistle \n flowering."
19,August,"Larvae of elephant \n and privet hawk-moths \n almost fully fed."
20,August,"The fungus Amanita \n mappa appears on \n sandy soil under \n oaks and beeches."
21,August,"Young bats begin \n to catch insects \n for themselves and \n no longer need \n their mothers’ milk."
22,August,"Smooth snakes are \n giving birth to \n live young."
23,August,"Winged ants appear \n in swarms from \n ants’ nests."
24,August,"Lapwings flock together \n for their autumnal \n migration."
25,August,"Flying alone and \n for the first \n time, young cuckoos \n are departing for \n Africa."
26,August,"Horn of plenty \n or “trumpet of \n death” fungus is \n appearing in woods."
27,August,"The adonis blue \n butterfly is on \n the wing."
28,August,"Caterpillars of the \n emperor moth are \n feeding on heather."
29,August,"Adult shrews are \n at the end \n of their lives \n and die of \n exhaustion."
30,August,"The first elder \n berries are ripe \n and are eaten \n by wood pigeons."
31,August,"Peacock butterflies can \n be found on \n the wing or \n resting."
01,September,"Death’s-head hawkmoths are \n on the wing."
02,September,"Many glistening inky \n cap fungi can \n be found."
03,September,"Blackberries start ripening."
04,September,"Young natterjack toads \n are leaving the \n water."
05,September,"Silk-button spangle galls \n are appearing on \n the back of \n oak leaves."
06,September,"Fancifully shaped knopper \n galls are falling \n from oaks."
07,September,"The last silver-spotted \n skippers can be \n spotted on the \n wing."
08,September,"Wasp nest beetles \n appear from underground \n wasps’ nests."
09,September,"Parasol fungi appear \n in meadows and \n along road sides."
10,September,"Crane flies or \n daddy longlegs are \n abundant."
11,September,"The first horse \n chestnuts are ripe \n and fall from \n the trees."
12,September,"Shaggy ink cap \n fungus appears on \n disturbed and nutrition-rich \n soils."
13,September,"The stemless dwarf \n thistle can still \n be found blooming."
14,September,"Lime trees begin \n to shed their \n leaves."
15,September,"Red deer stags \n start their mating \n season rutting."
16,September,"Common kingfishers can \n be spotted frequently."
17,September,"The first acorns \n are falling."
18,September,"Bracken assumes its \n autumnal tinting."
19,September,"Male badgers are \n preparing their burrows \n to accommodate multiple \n females."
20,September,"The first barn \n swallows and martins \n start their migration \n south."
21,September,"Beech-nuts are now \n plentiful in the \n woods."
22,September,"Ivy is beginning \n to bloom."
23,September,"Mistle thrushes are \n feeding on ripe \n orange rowan berries."
24,September,"Caddis fly are \n swarming over ponds \n in the evening."
25,September,"Turtle doves are \n leaving to spend \n the winter in \n West Africa."
26,September,"Second flowering of \n honeysuckle."
27,September,"False truffles can \n be seen in \n pine woods, after \n rabbits have dug \n them up."
28,September,"Dormice and squirrels \n are stocking up \n their winter supplies."
29,September,"Scarlet waxcap fungi \n are appearing in \n fields and on \n lawns."
30,September,"Migrating silver Y \n moths are on \n their way south."
01,October,"Adult eels are \n migrating from inland \n waters to the \n sea on their \n way to their \n spawning grounds in \n the Sargasso Sea."
02,October,"Many trees, including \n beeches, are changing \n colour to autumn \n tints."
03,October,"Hips, haws and \n sloes are now \n ripe."
04,October,"Field mushrooms in \n striking fairy-rings are \n in fields and \n on lawns."
05,October,"Rutting red deer \n are using their \n antlers in the \n competition for hinds."
06,October,"Fly agaric are \n emerging under birches \n and other trees."
07,October,"Starlings are starting \n to roost in \n huge flocks."
08,October,"The last flights \n of the green-veined \n white butterfly before \n it hibernates as \n a pupa."
09,October,"Queen wasps are \n going into hibernation."
10,October,"Blackbirds are feeding \n on fallen apples."
11,October,"Ladybird beetles are \n going into hibernation, \n often in homes."
12,October,"The trees are \n shedding their leaves \n but oak and \n ash trees are \n still very green."
13,October,"Cauliflower fungus is \n appearing at the \n base of Scots \n pine trunks."
14,October,"Chaffinches and lesser \n redpolls are sometimes \n singing on fine \n mornings."
15,October,"Wrens are beginning \n their autumn singing."
16,October,"The last martins \n and barn swallows \n are leaving to \n spend the winter \n in Africa."
17,October,"Dogwood leaves are \n turning a beautiful \n red."
18,October,"At dusk blackbirds \n are making their \n short high pitch \n alarm calls."
19,October,"Some young wood \n pigeons are leaving \n the nest only \n now."
20,October,"Amphibians start withdrawing \n into their hibernation \n shelters."
21,October,"The vomiting russula \n or the sickener \n fungus is appearing \n on damp, acid \n soils."
22,October,"The northern red \n oak takes on \n a striking red."
23,October,"The first fieldfares \n are arriving from \n the high north."
24,October,"Brent geese are \n returning from their \n northern breeding grounds \n with their young."
25,October,"Slowworms are going \n into hibernation, hidden \n in humus and \n rough grasses."
26,October,"The first woodcocks \n are arriving from \n Finland and Russia \n to spend the \n winter here."
27,October,"Comma butterflies have \n stopped flying for \n this year."
28,October,"The birch leaves \n have taken on \n their autumnal colours."
29,October,"Peacock butterflies stop \n flying as autumn \n progresses."
30,October,"Dormice are going \n into hibernation until \n April."
31,October,"Virtually all butterflies \n have stopped flying \n because of the \n cold."
01,November,"Mistle thrushes begin \n singing again from \n treetops."
02,November,"The brown long-eared \n bat starts to \n hibernate in trees, \n hollow walls, caves \n and mines."
03,November,"The grass stops \n growing."
04,November,"Money spiders in \n vast numbers on \n fields cover the \n grass with threads \n of silk."
05,November,"Autumnal leaf tinting \n is usually at \n its best about \n this time."
06,November,"Mermaids purses holding \n shark’s or skate’s \n eggs, wash up \n on beaches."
07,November,"Serotine bats are \n spending the winter \n in cavity walls, \n under roof tiles \n and in disused \n chimneys."
08,November,"Salmon start to \n ascend rivers from \n the sea to \n spawn upstream."
09,November,"The last red \n admiral butterflies are \n still on wing."
10,November,"Thousands of wild \n geese are back \n from their summer \n breeding grounds in \n the Arctic."
11,November,"Adult shrews die \n of exhaustion, the \n young are left \n to survive the \n winter."
12,November,"Frogs hibernate in \n the unfrozen muddy \n layer on the \n bottom of ponds \n and pools."
13,November,"Candlesnuff fungus is \n abundant on old \n stumps."
14,November,"The colourful butter \n waxcap appears in \n meadows."
15,November,"The spitting spider \n Scytodes thoracica goes \n hunting by night."
16,November,"Adders and grass \n snakes go into \n hibernation."
17,November,"Hedgehogs go into \n hibernation until April."
18,November,"Lapwings are feeding \n in flocks on \n fields."
19,November,"Brown witch’s butter \n fungus or jelly \n leaf is growing \n on dead birch \n and oak branches."
20,November,"Occasional appearance of \n brimstone butterflies."
21,November,"Squirrels retire to \n their winter retreats."
22,November,"Most moths start \n to hibernate as \n a pupa among \n fallen leaves or \n other hidden spots."
23,November,"Long-eared owls form \n communal roosts."
24,November,"Greenfinches assemble in \n flocks for their \n collective wintering."
25,November,"Common bracket fungus \n is abundant on \n dead wood."
26,November,"The pedunculate or \n English oaks are \n now completely bare."
27,November,"The nettle cells \n of stinging-nettles are \n losing strength."
28,November,"The Fluted bird’s \n nest fungus ejects \n its spores."
28,November,"Young magpies without \n a territory are \n roosting in small \n flocks."
30,November,"Pipistrelle bats are \n going into hibernation."
01,December,"Today the meteorological \n winter begins."
02,December,"The common shrew \n is now underground \n and hunting for \n invertebrates."
03,December,"Male foxes are \n calling in the \n night to find \n a female to \n mate with."
04,December,"Nathusius’ pipistrelle bats \n may fly on \n mild winter days."
05,December,"Red-stemmed feather moss \n abundant on sandy \n soil."
06,December,"The rough-mantled doris \n sea slug is \n looking for barnacles \n to feed on \n during its breeding \n time."
07,December,"Yellowhammers are congregating \n in winter flocks \n at nutrition-rich \n places."
08,December,"At night luminous \n centipedes can be \n spotted."
09,December,"The first young \n of grey seals \n are being born."
10,December,"Blackbirds clear circles \n of dead leaves \n to get at \n insects and worms \n in the ground."
11,December,"The song thrush \n sings at dawn \n in mild weather."
12,December,"Titmice extract larvae \n from oak marble \n galls and eat \n them."
13,December,"Groundsel can be \n seen in flower, \n in sheltered places \n all year long."
14,December,"Stoats have their \n white coat for \n winter."
15,December,"The mating season \n of squirrels has \n begun."
16,December,"The high, sharp \n call of the \n great spotted woodpecker \n can be heard \n high up in \n the trees."
17,December,"Shepherd’s purse is \n occasionally still flowering."
18,December,"Many insects winter \n in the hollow \n stems of dead \n plants."
19,December,"The first scarlet \n elf cup fungi \n appear."
20,December,"Long-tailed tit flocks \n are looking for \n food all day \n to survive."
21,December,"Common chickweed is \n occasionally still flowering."
22,December,"Compass jellyfish come \n near to the \n shore."
23,December,"Slowworms can be \n spotted in sunny \n weather."
24,December,"Early nuthatches commence \n their spring whistle."
25,December,"Stag beetles can \n be spotted on \n a clear evening."
26,December,"Yellow witch’s - \n butter fungus can \n be seen on \n the stems of \n dead oak and \n other trees."
27,December,"Yellow gorse is \n flowering profusely."
28,December,"Moles throw up \n hillocks when the \n ground is not \n frozen hard."
29,December,"Robins are singing."
30,December,"Wild boars churn \n up the fallen \n leaves looking for \n acorns."
31,December,"Earthworms tug/pull dead \n leaves into their \n holes and eat \n them."
01,January,"Badgers are asleep \n deep underground."
02,January,"Dunnocks commence their \n birdsong."
03,January,"The black-spotted chestnut \n moth can be \n spotted flying in \n the night."
04,January,"Marsh tits begins \n to sing."
05,January,"Beavers are satisfying \n their appetite with \n willow bark."
06,January,"Rabbits gnaw the \n bark of holly \n and other scrubs \n if the weather \n is severe."
07,January,"Stock doves can \n be heard calling."
08,January,"Smooth newts begin \n breeding if the \n weather is warm \n enough."
09,January,"Rabbits start devoting \n themselves to breeding."
10,January,"Lesser spotted woodpecker \n sometimes drums."
11,January,"Red dead-nettle already \n flowering here and \n there."
12,January,"The pale brindled \n beauty moth flies \n from now till \n late April."
13,January,"Swan’s-neck thread moss \n is forming its \n reproductive organs."
14,January,"Common winter damselflies \n on wing on \n warm days."
15,January,"First yellow daffodils \n are flowering."
16,January,"The first buntings \n start singing."
17,January,"Dark green cushions \n of broom fork-moss \n are growing on \n sandy banks and \n tree trunks."
18,January,"The loudest singers \n now are the \n great tits."
19,January,"Brown hairstreak butterflies \n are laying eggs \n in blackthorn bushes."
20,January,"Beavers are starting \n their mating season."
21,January,"Wood larks are \n singing."
22,January,"Black witch’s butter \n fungus (Exidia glandulosa) \n is growing on \n dead branches."
23,January,"Dumbledore beetle appears."
24,January,"First snowdrop leaves \n are emerging from \n the snow."
25,January,"Early skylarks start \n singing."
26,January,"Nathusius’ pipistrelle bats \n may be spotted \n flying if it \n is not too \n cold."
27,January,"Hare mating season \n begins and continues \n well into summer."
28,January,"The first robins \n start building their \n nests."
29,January,"Winter gnats abound."
30,January,"The first snowdrops \n begin to flower."
31,January,"Earthworms lie out."
01,February,"Small tortoiseshell butterflies \n start to emerge \n from hibernation."
02,February,"Greenfinches separate from \n flocks to continue \n on their own."
03,February,"Moles prepare their \n underground nests for \n their young."
04,February,"Tree creepers commence \n their spring call."
05,February,"Tawny owls hoot \n at dusk."
06,February,"Hawfinches feed on \n holly berries."
07,February,"Blackbirds sing at \n dusk."
08,February,"Winter jasmine is \n flowering profusely."
09,February,"Collared doves are \n cooing loudly in \n the morning."
10,February,"First crop of \n glistening ink cap \n fungus appears on \n dead broad-leaved \n trees."
11,February,"Greater spotted woodpeckers \n drum to mark \n their territory."
12,February,"Male moles in \n search for a \n partner dig long \n tunnels throwing up \n many hillocks."
13,February,"Badgers are giving \n birth to young."
14,February,"Woodcocks are making \n their flight displays \n ‘roding’, to mark \n their breeding territory."
15,February,"Yellowhammer starts to \n sing its characteristically \n shrill notes."
16,February,"Barn owls are \n mating."
17,February,"Peacock and brimstone \n butterflies emerge from \n hibernation."
18,February,"First primroses appearing."
19,February,"The great crested \n grebe’s mirror courtship \n dance begins."
20,February,"Salmon start to \n descend rivers on \n their migration to \n the sea."
21,February,"Frogs are busy \n mating and producing \n frogspawn."
22,February,"Chaffinches commence singing."
23,February,"Lesser periwinkle blooming \n with brightly blue \n flowers."
24,February,"Goldcrests begin their \n almost inaudibly high \n chirping."
25,February,"Adders emerge from \n hibernation."
26,February,"Brent geese start \n to leave for \n the Arctic islands."
27,February,"Early-nesting herons already \n have eggs."
28,February,"Slowworms revive from \n torpidity."
01,March,"Most tawny owls \n have laid their \n eggs."
02,March,"Wood anemones in \n flower in woodland."
03,March,"The first queen \n wasps emerge from \n hibernation."
04,March,"Willows and marsh-marigolds \n in flower."
05,March,"Curlews begin their \n display flights, rising \n steeply then gliding \n down while singing."
06,March,"Mistle thrushes are \n nesting."
07,March,"Blackthorn in flower."
08,March,"Early swans may \n start building their \n nest."
09,March,"First lesser celandine \n flowers appearing."
10,March,"Male hares start \n to fight, standing \n on hind legs \n and boxing."
11,March,"The first generation \n of brimstone butterflies \n start their flight \n period."
12,March,"Male yews begin \n shedding abundant amounts \n pollen."
13,March,"The large white \n butterflies are on \n the wing."
14,March,"Sparrowhawks can be \n seen soaring over \n their territories only \n at this time \n of year."
15,March,"Common frogs start \n to emerge."
16,March,"Black ants remove \n the seal from \n the entrance to \n the nest and \n begin to forage \n above ground."
17,March,"The first speckled \n wood butterflies can \n be spotted flying."
18,March,"Common frogs start \n croaking to attract \n the attention of \n females."
19,March,"Wrens are singing \n higher in the \n trees, their voices \n carrying further."
20,March,"The first young \n European pine martens \n are born."
21,March,"The first newts \n return to the \n water."
22,March,"Rosemary has started \n flowering."
23,March,"First horse chestnut \n leaves are unfolding."
24,March,"Toads are mating \n and laying eggs."
25,March,"Kingfishers are looking \n for nesting holes."
26,March,"First hazel leaves \n are appearing."
28,March,"Magnolia flowering before \n the first leaves \n appear."
22,March,"Wheatears have arrived, \n one of the \n first long-distance migrant \n birds to return."
30,March,"Long-eared owls are \n nesting."
31,March,"Crows, jackdaws, magpies \n and rooks are \n building or repairing \n their nests."
01,April,"Mating season has \n started for adders; \n the males compete \n in a dance/fight \n to impress females."
02,April,"The first Chiffchaffs \n have returned and \n begin to sing \n their name."
03,April,"The first young \n of the wild \n boar are born."
04,April,"First willow warbler \n song can be \n heard."
05,April,"Tadpoles abound in \n ponds and pools."
06,April,"Sparrowhawks and kestrels \n nesting."
07,April,"The first nightingale \n returns."
08,April,"Most buzzards have \n laid their first \n egg."
09,April,"The distinctive orange-tip \n butterflies are flying."
10,April,"Grass snakes are \n mating."
11,April,"Cuckoo males begin \n to arrive from \n Sub-Saharan Africa and \n start calling their \n name."
12,April,"Beavers are having \n their first young."
13,April,"Ash trees are \n flowering."
14,April,"Yellow wagtails have \n arrived from their \n winter retreats."
15,April,"Hedgehogs are emerging \n from hibernation."
16,April,"Small tortoiseshell butterfly \n and comma butterfly \n are at the \n peak of their \n flight period."
17,April,"Young mallards are \n hatching and can \n be seen swimming."
18,April,"Crab apples flowering."
19,April,"Grey squirrels prepare \n their dreys (tree \n nests)."
20,April,"Yellow archangel in \n flower."
21,April,"Sandpipers, European pied \n flycatchers, grasshopper warblers \n and many other \n birds have returned \n to the country."
22,April,"Pedunculate or English \n oak leaves unfolding."
23,April,"Hawthorn starts flowering."
24,April,"The wood warbler \n has arrived to \n spend the summer."
25,April,"Great and blue \n tits are now \n sitting on eggs."
26,April,"Rare migrating turtle \n doves that have \n survived being hunted \n while crossing Malta \n arrive in UK."
27,April,"First flowers of \n the horse chestnut \n tree appearing."
22,April,"The reed warbler \n is in the \n country."
29,April,"The first swift \n has arrived and \n will stay for \n  one hundred days."
30,April,"The male wren \n  is busy making \n  several nests, the \n  female chooses one \n of them."""

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
        draw.text((20, 100), get_message_for_day(data_with_numbers), font = font18, fill = 0)
        epd.display_Partial(epd.getbuffer(Himage))