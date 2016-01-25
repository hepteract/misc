# coding: utf8
"""
    Use Markov chains to generate random text that sounds Japanese.
    This makes random pronounceable passwords that are both strong and easy
    to memorize.
    
    Of course English or any other language could be used in the sample text.
    
    See more details at http://exyr.org/2011/random-pronounceable-passwords/
    
    Author: Simon Sapin
    License: BSD
"""

from __future__ import division
import string
import itertools
import random
from collections import defaultdict


# This is a romanization of the opening of "Genji Monogatari"
# by Murasaki Shikibu.
# Source: http://etext.lib.virginia.edu/japanese/genji/roman.html
japanese = '''
Idure no ohom-toki ni ka, nyougo, kaui amata saburahi tamahi keru naka ni,
ito yamgotonaki kiha ni ha ara nu ga, sugurete tokimeki tamahu ari keri.
Hazime yori ware ha to omohi agari tamahe ru ohom-kata-gata, mezamasiki mono ni
otosime sonemi tamahu. Onazi hodo, sore yori gerahu no kaui-tati ha, masite 
yasukara zu. Asa-yuhu no miya-dukahe ni tuke te mo, hito no kokoro wo nomi 
ugokasi, urami wo ohu tumori ni ya ari kem, ito atusiku nari yuki, mono kokoro-
boso-ge ni sato-gati naru wo, iyo-iyo aka zu ahare naru mono ni omohosi te hito 
no sosiri wo mo e habakara se tamaha zu, yo no tamesi ni mo nari nu beki ohom-
motenasi nari.
Kamdatime, uhe-bito nado mo, ainaku me wo sobame tutu, "Ito mabayuki hito no 
ohom-oboye nari. Morokosi ni mo, kakaru koto no okori ni koso, yo mo midare, 
asikari kere" to, yau-yau amenosita ni mo adikinau, hito no mote-nayami-gusa ni 
nari te, Yauki-hi no tamesi mo hiki ide tu beku nariyuku ni, ito hasitanaki koto 
ohokare do, katazikenaki mi-kokoro-bahe no taguhi naki wo tanomi ni te mazirahi 
tamahu.
TiTi no Dainagon ha nakunari te haha Kita-no-kata nam inisihe no yosi aru ni te, 
oya uti-gusi, sasi-atari te yo no oboye hanayaka naru ohom-kata-gata ni mo itau 
otora zu, nani-goto no gisiki wo mo motenasi tamahi kere do, tori-tate te haka-
bakasiki usiro-mi si nakere ba, koto aru toki ha, naho yori-dokoro naku kokoro-
boso-ge nari.
Saki no yo ni mo ohom-tigiri ya hukakari kem, yo ni naku kiyora naru tama no 
wonoko miko sahe umare tamahi nu. Itusika to kokoro-motonagara se tamahi te, 
isogi mawirase te go-ran-zuru ni, meduraka naru tigo no ohom-katati nari.
Iti-no-Miko ha, Udaizin no Nyougo no ohom-hara ni te, yose omoku, utagahi naki 
Mauke-no-kimi to, yo ni mote-kasiduki kikoyure do, kono ohom-nihohi ni ha narabi 
tamahu beku mo ara zari kere ba, ohokata no yamgotonaki ohom-omohi ni te, kono 
Kimi wo ba, watakusi-mono ni omohosi kasiduki tamahu koto kagiri nasi.
Hazime yori osinabete no uhe-miya-dukahe si tamahu beki kiha ni ha ara zari ki. 
Oboye ito yamgotonaku, zyauzu-mekasi kere do, warinaku matuhasa se tamahu amari 
ni, sarubeki ohom-asobi no wori-wori, nani-goto ni mo yuwe aru koto no husi-busi 
ni ha, madu mau-nobora se tamahu. Aru-toki ni ha ohotono-gomori sugusi te, 
yagate saburahase tamahi nado, anagati ni o-mahe sara zu mote-nasa se tamahi si 
hodo ni, onodukara karoki kata ni mo miye si wo, kono Miko umare tamahi te noti 
ha, ito kokoro koto ni omohosi oki te tare ba, Bau ni mo, you se zu ha, kono
Miko no wi tamahu beki na'meri to, Ichi-no-Miko no Nyougo ha obosi utagahe ri. 
Hito yori saki ni mawiri tamahi te, yamgotonaki ohom-omohi nabete nara zu, Miko-
tati nado mo ohasimase ba, kono Ohom-kata no ohom-isame wo nomi zo, naho 
wadurahasiu kokoro-gurusiu omohi kikoye sase tamahi keru.
 
Kasikoki mi-kage wo ba tanomi kikoye nagara, otosime kizu wo motome tamahu hito 
ha ohoku, waga mi ha ka-yowaku mono-hakanaki arisama ni te, naka-naka naru mono-
omohi wo zo si tamahu. Mi-tubone ha Kiritubo nari. Amata no ohom-Kata-gata wo 
sugi sase tamahi te, hima naki o-mahe-watari ni, hito no mi-kokoro wo tukusi 
tamahu mo, geni kotowari to miye tari. Mau-nobori tamahu ni mo, amari uti-sikiru 
wori-wori ha, uti-hasi, wata-dono no koko kasiko no miti ni, ayasiki waza wo si 
tutu, ohom-okuri mukahe no hito no kinu no suso, tahe gataku, masanaki koto mo 
ari. Mata aru toki ni ha, e sara nu me-dau no to wo sasi-kome, konata kanata 
kokoro wo ahase te, hasitaname wadurahase tamahu toki mo ohokari. Koto ni hure 
te kazu sira zu kurusiki koto nomi masare ba, ito itau omohi wabi taru wo, itodo 
ahare to go-ran-zi te, Kourau-den ni motoyori saburahi tamahu Kaui no zausi wo 
hoka ni utusa se tamahi te, Uhe-tubone ni tamaha su. Sono urami masite yara m 
kata nasi.
'''

frankenstein = '''I am by birth a Genevese, and my family is one of the most distinguished of that republic. My ancestors had been for many years counsellors and syndics, and my father had filled several public situations with honour and reputation. He was respected by all who knew him for his integrity and indefatigable attention to public business. He passed his younger days perpetually occupied by the affairs of his country; a variety of circumstances had prevented his marrying early, nor was it until the decline of life that he became a husband and the father of a family.
As the circumstances of his marriage illustrate his character, I cannot refrain from relating them. One of his most intimate friends was a merchant who, from a flourishing state, fell, through numerous mischances, into poverty. This man, whose name was Beaufort, was of a proud and unbending disposition and could not bear to live in poverty and oblivion in the same country where he had formerly been distinguished for his rank and magnificence. Having paid his debts, therefore, in the most honourable manner, he retreated with his daughter to the town of Lucerne, where he lived unknown and in wretchedness. My father loved Beaufort with the truest friendship and was deeply grieved by his retreat in these unfortunate circumstances. He bitterly deplored the false pride which led his friend to a conduct so little worthy of the affection that united them. He lost no time in endeavouring to seek him out, with the hope of persuading him to begin the world again through his credit and assistance. Beaufort had taken effectual measures to conceal himself, and it was ten months before my father discovered his abode. Overjoyed at this discovery, he hastened to the house, which was situated in a mean street near the Reuss. But when he entered, misery and despair alone welcomed him. Beaufort had saved but a very small sum of money from the wreck of his fortunes, but it was sufficient to provide him with sustenance for some months, and in the meantime he hoped to procure some respectable employment in a merchant’s house. The interval was, consequently, spent in inaction; his grief only became more deep and rankling when he had leisure for reflection, and at length it took so fast hold of his mind that at the end of three months he lay on a bed of sickness, incapable of any exertion.
His daughter attended him with the greatest tenderness, but she saw with despair that their little fund was rapidly decreasing and that there was no other prospect of support. But Caroline Beaufort possessed a mind of an uncommon mould, and her courage rose to support her in her adversity. She procured plain work; she plaited straw and by various means contrived to earn a pittance scarcely sufficient to support life.
Several months passed in this manner. Her father grew worse; her time was more entirely occupied in attending him; her means of subsistence decreased; and in the tenth month her father died in her arms, leaving her an orphan and a beggar. This last blow overcame her, and she knelt by Beaufort’s coffin weeping bitterly, when my father entered the chamber. He came like a protecting spirit to the poor girl, who committed herself to his care; and after the interment of his friend he conducted her to Geneva and placed her under the protection of a relation. Two years after this event Caroline became his wife.
There was a considerable difference between the ages of my parents, but this circumstance seemed to unite them only closer in bonds of devoted affection. There was a sense of justice in my father’s upright mind which rendered it necessary that he should approve highly to love strongly. Perhaps during former years he had suffered from the late-discovered unworthiness of one beloved and so was disposed to set a greater value on tried worth. There was a show of gratitude and worship in his attachment to my mother, differing wholly from the doting fondness of age, for it was inspired by reverence for her virtues and a desire to be the means of, in some degree, recompensing her for the sorrows she had endured, but which gave inexpressible grace to his behaviour to her. Everything was made to yield to her wishes and her convenience. He strove to shelter her, as a fair exotic is sheltered by the gardener, from every rougher wind and to surround her with all that could tend to excite pleasurable emotion in her soft and benevolent mind. Her health, and even the tranquillity of her hitherto constant spirit, had been shaken by what she had gone through. During the two years that had elapsed previous to their marriage my father had gradually relinquished all his public functions; and immediately after their union they sought the pleasant climate of Italy, and the change of scene and interest attendant on a tour through that land of wonders, as a restorative for her weakened frame.
From Italy they visited Germany and France. I, their eldest child, was born at Naples, and as an infant accompanied them in their rambles. I remained for several years their only child. Much as they were attached to each other, they seemed to draw inexhaustible stores of affection from a very mine of love to bestow them upon me. My mother’s tender caresses and my father’s smile of benevolent pleasure while regarding me are my first recollections. I was their plaything and their idol, and something better — their child, the innocent and helpless creature bestowed on them by heaven, whom to bring up to good, and whose future lot it was in their hands to direct to happiness or misery, according as they fulfilled their duties towards me. With this deep consciousness of what they owed towards the being to which they had given life, added to the active spirit of tenderness that animated both, it may be imagined that while during every hour of my infant life I received a lesson of patience, of charity, and of self-control, I was so guided by a silken cord that all seemed but one train of enjoyment to me. For a long time I was their only care. My mother had much desired to have a daughter, but I continued their single offspring. When I was about five years old, while making an excursion beyond the frontiers of Italy, they passed a week on the shores of the Lake of Como. Their benevolent disposition often made them enter the cottages of the poor. This, to my mother, was more than a duty; it was a necessity, a passion — remembering what she had suffered, and how she had been relieved — for her to act in her turn the guardian angel to the afflicted. During one of their walks a poor cot in the foldings of a vale attracted their notice as being singularly disconsolate, while the number of half-clothed children gathered about it spoke of penury in its worst shape. One day, when my father had gone by himself to Milan, my mother, accompanied by me, visited this abode. She found a peasant and his wife, hard working, bent down by care and labour, distributing a scanty meal to five hungry babes. Among these there was one which attracted my mother far above all the rest. She appeared of a different stock. The four others were dark-eyed, hardy little vagrants; this child was thin and very fair. Her hair was the brightest living gold, and despite the poverty of her clothing, seemed to set a crown of distinction on her head. Her brow was clear and ample, her blue eyes cloudless, and her lips and the moulding of her face so expressive of sensibility and sweetness that none could behold her without looking on her as of a distinct species, a being heaven-sent, and bearing a celestial stamp in all her features. The peasant woman, perceiving that my mother fixed eyes of wonder and admiration on this lovely girl, eagerly communicated her history. She was not her child, but the daughter of a Milanese nobleman. Her mother was a German and had died on giving her birth. The infant had been placed with these good people to nurse: they were better off then. They had not been long married, and their eldest child was but just born. The father of their charge was one of those Italians nursed in the memory of the antique glory of Italy — one among the schiavi ognor frementi, who exerted himself to obtain the liberty of his country. He became the victim of its weakness. Whether he had died or still lingered in the dungeons of Austria was not known. His property was confiscated; his child became an orphan and a beggar. She continued with her foster parents and bloomed in their rude abode, fairer than a garden rose among dark-leaved brambles. When my father returned from Milan, he found playing with me in the hall of our villa a child fairer than pictured cherub — a creature who seemed to shed radiance from her looks and whose form and motions were lighter than the chamois of the hills. The apparition was soon explained. With his permission my mother prevailed on her rustic guardians to yield their charge to her. They were fond of the sweet orphan. Her presence had seemed a blessing to them, but it would be unfair to her to keep her in poverty and want when Providence afforded her such powerful protection. They consulted their village priest, and the result was that Elizabeth Lavenza became the inmate of my parents’ house — my more than sister — the beautiful and adored companion of all my occupations and my pleasures.
Everyone loved Elizabeth. The passionate and almost reverential attachment with which all regarded her became, while I shared it, my pride and my delight. On the evening previous to her being brought to my home, my mother had said playfully, “I have a pretty present for my Victor — tomorrow he shall have it.” And when, on the morrow, she presented Elizabeth to me as her promised gift, I, with childish seriousness, interpreted her words literally and looked upon Elizabeth as mine — mine to protect, love, and cherish. All praises bestowed on her I received as made to a possession of my own. We called each other familiarly by the name of cousin. No word, no expression could body forth the kind of relation in which she stood to me — my more than sister, since till death she was to be mine only.

We were brought up together; there was not quite a year difference in our ages. I need not say that we were strangers to any species of disunion or dispute. Harmony was the soul of our companionship, and the diversity and contrast that subsisted in our characters drew us nearer together. Elizabeth was of a calmer and more concentrated disposition; but, with all my ardour, I was capable of a more intense application and was more deeply smitten with the thirst for knowledge. She busied herself with following the aerial creations of the poets; and in the majestic and wondrous scenes which surrounded our Swiss home — the sublime shapes of the mountains, the changes of the seasons, tempest and calm, the silence of winter, and the life and turbulence of our Alpine summers — she found ample scope for admiration and delight. While my companion contemplated with a serious and satisfied spirit the magnificent appearances of things, I delighted in investigating their causes. The world was to me a secret which I desired to divine. Curiosity, earnest research to learn the hidden laws of nature, gladness akin to rapture, as they were unfolded to me, are among the earliest sensations I can remember.
On the birth of a second son, my junior by seven years, my parents gave up entirely their wandering life and fixed themselves in their native country. We possessed a house in Geneva, and a campagne on Belrive, the eastern shore of the lake, at the distance of rather more than a league from the city. We resided principally in the latter, and the lives of my parents were passed in considerable seclusion. It was my temper to avoid a crowd and to attach myself fervently to a few. I was indifferent, therefore, to my school-fellows in general; but I united myself in the bonds of the closest friendship to one among them. Henry Clerval was the son of a merchant of Geneva. He was a boy of singular talent and fancy. He loved enterprise, hardship, and even danger for its own sake. He was deeply read in books of chivalry and romance. He composed heroic songs and began to write many a tale of enchantment and knightly adventure. He tried to make us act plays and to enter into masquerades, in which the characters were drawn from the heroes of Roncesvalles, of the Round Table of King Arthur, and the chivalrous train who shed their blood to redeem the holy sepulchre from the hands of the infidels.
No human being could have passed a happier childhood than myself. My parents were possessed by the very spirit of kindness and indulgence. We felt that they were not the tyrants to rule our lot according to their caprice, but the agents and creators of all the many delights which we enjoyed. When I mingled with other families I distinctly discerned how peculiarly fortunate my lot was, and gratitude assisted the development of filial love.
My temper was sometimes violent, and my passions vehement; but by some law in my temperature they were turned not towards childish pursuits but to an eager desire to learn, and not to learn all things indiscriminately. I confess that neither the structure of languages, nor the code of governments, nor the politics of various states possessed attractions for me. It was the secrets of heaven and earth that I desired to learn; and whether it was the outward substance of things or the inner spirit of nature and the mysterious soul of man that occupied me, still my inquiries were directed to the metaphysical, or in it highest sense, the physical secrets of the world.
Meanwhile Clerval occupied himself, so to speak, with the moral relations of things. The busy stage of life, the virtues of heroes, and the actions of men were his theme; and his hope and his dream was to become one among those whose names are recorded in story as the gallant and adventurous benefactors of our species. The saintly soul of Elizabeth shone like a shrine-dedicated lamp in our peaceful home. Her sympathy was ours; her smile, her soft voice, the sweet glance of her celestial eyes, were ever there to bless and animate us. She was the living spirit of love to soften and attract; I might have become sullen in my study, through the ardour of my nature, but that she was there to subdue me to a semblance of her own gentleness. And Clerval — could aught ill entrench on the noble spirit of Clerval? Yet he might not have been so perfectly humane, so thoughtful in his generosity, so full of kindness and tenderness amidst his passion for adventurous exploit, had she not unfolded to him the real loveliness of beneficence and made the doing good the end and aim of his soaring ambition.
I feel exquisite pleasure in dwelling on the recollections of childhood, before misfortune had tainted my mind and changed its bright visions of extensive usefulness into gloomy and narrow reflections upon self. Besides, in drawing the picture of my early days, I also record those events which led, by insensible steps, to my after tale of misery, for when I would account to myself for the birth of that passion which afterwards ruled my destiny I find it arise, like a mountain river, from ignoble and almost forgotten sources; but, swelling as it proceeded, it became the torrent which, in its course, has swept away all my hopes and joys. Natural philosophy is the genius that has regulated my fate; I desire, therefore, in this narration, to state those facts which led to my predilection for that science. When I was thirteen years of age we all went on a party of pleasure to the baths near Thonon; the inclemency of the weather obliged us to remain a day confined to the inn. In this house I chanced to find a volume of the works of Cornelius Agrippa. I opened it with apathy; the theory which he attempts to demonstrate and the wonderful facts which he relates soon changed this feeling into enthusiasm. A new light seemed to dawn upon my mind, and bounding with joy, I communicated my discovery to my father. My father looked carelessly at the title page of my book and said, “Ah! Cornelius Agrippa! My dear Victor, do not waste your time upon this; it is sad trash.”
If, instead of this remark, my father had taken the pains to explain to me that the principles of Agrippa had been entirely exploded and that a modern system of science had been introduced which possessed much greater powers than the ancient, because the powers of the latter were chimerical, while those of the former were real and practical, under such circumstances I should certainty have thrown Agrippa aside and have contented my imagination, warmed as it was, by returning with greater ardour to my former studies. It is even possible that the train of my ideas would never have received the fatal impulse that led to my ruin. But the cursory glance my father had taken of my volume by no means assured me that he was acquainted with its contents, and I continued to read with the greatest avidity. When I returned home my first care was to procure the whole works of this author, and afterwards of Paracelsus and Albertus Magnus. I read and studied the wild fancies of these writers with delight; they appeared to me treasures known to few besides myself. I have described myself as always having been imbued with a fervent longing to penetrate the secrets of nature. In spite of the intense labour and wonderful discoveries of modern philosophers, I always came from my studies discontented and unsatisfied. Sir Isaac Newton is said to have avowed that he felt like a child picking up shells beside the great and unexplored ocean of truth. Those of his successors in each branch of natural philosophy with whom I was acquainted appeared even to my boy’s apprehensions as tyros engaged in the same pursuit.
The untaught peasant beheld the elements around him and was acquainted with their practical uses. The most learned philosopher knew little more. He had partially unveiled the face of Nature, but her immortal lineaments were still a wonder and a mystery. He might dissect, anatomize, and give names; but, not to speak of a final cause, causes in their secondary and tertiary grades were utterly unknown to him. I had gazed upon the fortifications and impediments that seemed to keep human beings from entering the citadel of nature, and rashly and ignorantly I had repined.
But here were books, and here were men who had penetrated deeper and knew more. I took their word for all that they averred, and I became their disciple. It may appear strange that such should arise in the eighteenth century; but while I followed the routine of education in the schools of Geneva, I was, to a great degree, self-taught with regard to my favourite studies. My father was not scientific, and I was left to struggle with a child’s blindness, added to a student’s thirst for knowledge. Under the guidance of my new preceptors I entered with the greatest diligence into the search of the philosopher’s stone and the elixir of life; but the latter soon obtained my undivided attention. Wealth was an inferior object, but what glory would attend the discovery if I could banish disease from the human frame and render man invulnerable to any but a violent death! Nor were these my only visions. The raising of ghosts or devils was a promise liberally accorded by my favourite authors, the fulfillment of which I most eagerly sought; and if my incantations were always unsuccessful, I attributed the failure rather to my own inexperience and mistake than to a want of skill or fidelity in my instructors. And thus for a time I was occupied by exploded systems, mingling, like an unadept, a thousand contradictory theories and floundering desperately in a very slough of multifarious knowledge, guided by an ardent imagination and childish reasoning, till an accident again changed the current of my ideas. When I was about fifteen years old we had retired to our house near Belrive, when we witnessed a most violent and terrible thunderstorm. It advanced from behind the mountains of Jura, and the thunder burst at once with frightful loudness from various quarters of the heavens. I remained, while the storm lasted, watching its progress with curiosity and delight. As I stood at the door, on a sudden I beheld a stream of fire issue from an old and beautiful oak which stood about twenty yards from our house; and so soon as the dazzling light vanished, the oak had disappeared, and nothing remained but a blasted stump. When we visited it the next morning, we found the tree shattered in a singular manner. It was not splintered by the shock, but entirely reduced to thin ribbons of wood. I never beheld anything so utterly destroyed.
Before this I was not unacquainted with the more obvious laws of electricity. On this occasion a man of great research in natural philosophy was with us, and excited by this catastrophe, he entered on the explanation of a theory which he had formed on the subject of electricity and galvanism, which was at once new and astonishing to me. All that he said threw greatly into the shade Cornelius Agrippa, Albertus Magnus, and Paracelsus, the lords of my imagination; but by some fatality the overthrow of these men disinclined me to pursue my accustomed studies. It seemed to me as if nothing would or could ever be known. All that had so long engaged my attention suddenly grew despicable. By one of those caprices of the mind which we are perhaps most subject to in early youth, I at once gave up my former occupations, set down natural history and all its progeny as a deformed and abortive creation, and entertained the greatest disdain for a would-be science which could never even step within the threshold of real knowledge. In this mood of mind I betook myself to the mathematics and the branches of study appertaining to that science as being built upon secure foundations, and so worthy of my consideration.
Thus strangely are our souls constructed, and by such slight ligaments are we bound to prosperity or ruin. When I look back, it seems to me as if this almost miraculous change of inclination and will was the immediate suggestion of the guardian angel of my life — the last effort made by the spirit of preservation to avert the storm that was even then hanging in the stars and ready to envelop me. Her victory was announced by an unusual tranquillity and gladness of soul which followed the relinquishing of my ancient and latterly tormenting studies. It was thus that I was to be taught to associate evil with their prosecution, happiness with their disregard.
It was a strong effort of the spirit of good, but it was ineffectual. Destiny was too potent, and her immutable laws had decreed my utter and terrible destruction.


When I had attained the age of seventeen my parents resolved that I should become a student at the university of Ingolstadt. I had hitherto attended the schools of Geneva, but my father thought it necessary for the completion of my education that I should be made acquainted with other customs than those of my native country. My departure was therefore fixed at an early date, but before the day resolved upon could arrive, the first misfortune of my life occurred — an omen, as it were, of my future misery. Elizabeth had caught the scarlet fever; her illness was severe, and she was in the greatest danger. During her illness many arguments had been urged to persuade my mother to refrain from attending upon her. She had at first yielded to our entreaties, but when she heard that the life of her favourite was menaced, she could no longer control her anxiety. She attended her sickbed; her watchful attentions triumphed over the malignity of the distemper — Elizabeth was saved, but the consequences of this imprudence were fatal to her preserver. On the third day my mother sickened; her fever was accompanied by the most alarming symptoms, and the looks of her medical attendants prognosticated the worst event. On her deathbed the fortitude and benignity of this best of women did not desert her. She joined the hands of Elizabeth and myself. “My children,” she said, “my firmest hopes of future happiness were placed on the prospect of your union. This expectation will now be the consolation of your father. Elizabeth, my love, you must supply my place to my younger children. Alas! I regret that I am taken from you; and, happy and beloved as I have been, is it not hard to quit you all? But these are not thoughts befitting me; I will endeavour to resign myself cheerfully to death and will indulge a hope of meeting you in another world.”
She died calmly, and her countenance expressed affection even in death. I need not describe the feelings of those whose dearest ties are rent by that most irreparable evil, the void that presents itself to the soul, and the despair that is exhibited on the countenance. It is so long before the mind can persuade itself that she whom we saw every day and whose very existence appeared a part of our own can have departed forever — that the brightness of a beloved eye can have been extinguished and the sound of a voice so familiar and dear to the ear can be hushed, never more to be heard. These are the reflections of the first days; but when the lapse of time proves the reality of the evil, then the actual bitterness of grief commences. Yet from whom has not that rude hand rent away some dear connection? And why should I describe a sorrow which all have felt, and must feel? The time at length arrives when grief is rather an indulgence than a necessity; and the smile that plays upon the lips, although it may be deemed a sacrilege, is not banished. My mother was dead, but we had still duties which we ought to perform; we must continue our course with the rest and learn to think ourselves fortunate whilst one remains whom the spoiler has not seized.
My departure for Ingolstadt, which had been deferred by these events, was now again determined upon. I obtained from my father a respite of some weeks. It appeared to me sacrilege so soon to leave the repose, akin to death, of the house of mourning and to rush into the thick of life. I was new to sorrow, but it did not the less alarm me. I was unwilling to quit the sight of those that remained to me, and above all, I desired to see my sweet Elizabeth in some degree consoled.
She indeed veiled her grief and strove to act the comforter to us all. She looked steadily on life and assumed its duties with courage and zeal. She devoted herself to those whom she had been taught to call her uncle and cousins. Never was she so enchanting as at this time, when she recalled the sunshine of her smiles and spent them upon us. She forgot even her own regret in her endeavours to make us forget.
The day of my departure at length arrived. Clerval spent the last evening with us. He had endeavoured to persuade his father to permit him to accompany me and to become my fellow student, but in vain. His father was a narrow-minded trader and saw idleness and ruin in the aspirations and ambition of his son. Henry deeply felt the misfortune of being debarred from a liberal education. He said little, but when he spoke I read in his kindling eye and in his animated glance a restrained but firm resolve not to be chained to the miserable details of commerce.
We sat late. We could not tear ourselves away from each other nor persuade ourselves to say the word “Farewell!” It was said, and we retired under the pretence of seeking repose, each fancying that the other was deceived; but when at morning’s dawn I descended to the carriage which was to convey me away, they were all there — my father again to bless me, Clerval to press my hand once more, my Elizabeth to renew her entreaties that I would write often and to bestow the last feminine attentions on her playmate and friend.
I threw myself into the chaise that was to convey me away and indulged in the most melancholy reflections. I, who had ever been surrounded by amiable companions, continually engaged in endeavouring to bestow mutual pleasure — I was now alone. In the university whither I was going I must form my own friends and be my own protector. My life had hitherto been remarkably secluded and domestic, and this had given me invincible repugnance to new countenances. I loved my brothers, Elizabeth, and Clerval; these were “old familiar faces,” but I believed myself totally unfitted for the company of strangers. Such were my reflections as I commenced my journey; but as I proceeded, my spirits and hopes rose. I ardently desired the acquisition of knowledge. I had often, when at home, thought it hard to remain during my youth cooped up in one place and had longed to enter the world and take my station among other human beings. Now my desires were complied with, and it would, indeed, have been folly to repent.
I had sufficient leisure for these and many other reflections during my journey to Ingolstadt, which was long and fatiguing. At length the high white steeple of the town met my eyes. I alighted and was conducted to my solitary apartment to spend the evening as I pleased.
The next morning I delivered my letters of introduction and paid a visit to some of the principal professors. Chance — or rather the evil influence, the Angel of Destruction, which asserted omnipotent sway over me from the moment I turned my reluctant steps from my father’s door — led me first to M. Krempe, professor of natural philosophy. He was an uncouth man, but deeply imbued in the secrets of his science. He asked me several questions concerning my progress in the different branches of science appertaining to natural philosophy. I replied carelessly, and partly in contempt, mentioned the names of my alchemists as the principal authors I had studied. The professor stared. “Have you,” he said, “really spent your time in studying such nonsense?”
I replied in the affirmative. “Every minute,” continued M. Krempe with warmth, “every instant that you have wasted on those books is utterly and entirely lost. You have burdened your memory with exploded systems and useless names. Good God! In what desert land have you lived, where no one was kind enough to inform you that these fancies which you have so greedily imbibed are a thousand years old and as musty as they are ancient? I little expected, in this enlightened and scientific age, to find a disciple of Albertus Magnus and Paracelsus. My dear sir, you must begin your studies entirely anew.”
'''


lorem_ipsum = '''Sit vide animal persecuti ex, ne lorem blandit oportere vix, purto soleat libris cu mei. Imperdiet hendrerit adolescens per ne. Odio debitis liberavisse ex qui, putent propriae accusata usu eu, ut ius quaeque maiorum delectus. In vix vocent singulis persequeris, an mei mazim fierent percipit, eu ius alii fastidii reprimique. Ei sumo partem fierent per.

Sale partem complectitur eam id, sint nullam accumsan in vel. Te per choro intellegebat. Ei ius repudiare efficiendi, delectus abhorreant usu ea. Est falli consequuntur ne. Labores concludaturque ei has.

Ne saperet facilisis eum, facete civibus eu nec. Scaevola lobortis usu te, cum offendit aliquando consetetur ut. In eam augue lobortis, nostrud delectus ad his, dicit cotidieque eam an. Ad dicam noster oblique usu, nullam accumsan no nec. Quo doming nemore efficiendi ad, te odio harum mediocritatem vix. Sint liberavisse pro an, pro viris aeterno ut. Tollit accumsan theophrastus an pri.

Te pro nonumy aperiri, vis justo homero ex. Eius dolores senserit at est. Suas veritus delicatissimi pri ad, id ius fugit eripuit labores. Mundi nostro suavitate per eu. Mea abhorreant assueverit ei, vis no atqui dicam, sea ferri percipitur eu.

Ne ius omnesque vivendum, quis legimus appellantur ne mei. Tempor impedit cotidieque ad vis. Ad utinam legere pri, ut ius nobis primis. Inani labitur constituam in eum. Sed ex summo mnesarchum, id saperet delectus vim, te mazim nullam sanctus eos.

Qui ea esse corpora suscipiantur, ex duo omnis quaestio. Brute assum sapientem duo cu, te sit labore indoctum. Idque invenire sit ad, eirmod feugait deserunt eum ei. Vis adversarium liberavisse eu. Ne est sint error minimum, vim at justo fugit nostro.

Sit ex dico facete, in eam probo persequeris. Consul cetero similique sit id, vix id etiam iuvaret epicurei. Assum copiosae volutpat sea at, in errem dolore sea, ex mollis nostrud qui. Te sit saperet suscipiantur. In qui option reformidans.

Ad vel veniam salutatus democritum, feugait consectetuer sit ex. Luptatum sententiae pro eu, in vix praesent intellegat voluptaria. Et eos doctus forensibus. Omnes aeterno inermis has no, dictas voluptatum assueverit eam ea. Ut duo periculis deterruisset. Ex sed nemore iuvaret necessitatibus.

Sonet admodum volumus eu eum, cum in idque suscipit accommodare. Ne liber accumsan similique mea, his wisi voluptatum intellegebat no, an per populo euismod sensibus. Est te dico fuisset. Bonorum consectetuer consequuntur mea ad, oportere sententiae adversarium ea usu.

Ei per quis democritum, fugit erroribus sea te. Tation abhorreant no vel, ne mundi imperdiet consequuntur nec. Nibh justo legendos id eam, in cum alia referrentur, vim liber recteque ei. Invenire quaerendum at vim, postea indoctum scripserit ius no.
'''

periodic = '''Hydrogen
Helium
Lithium
Beryillium
Boron
Carbon
Nitrogen
Oxygen
Fluorine
Neon
Sodium
Magnesium
Aluminium
Silicon
Phosphorus
Sulfur
Chlorine
Argon
Potassium
Calcium
Scandium
Titanium
Tritanium
Chromium
Iron
Cobalt
Nickel
Copper
Zinc
Gallium
Germanium
Arsenic
Selenium
Bromine
Krypton
Rubidium
Strontium
Silver
Tin
Iodine
Xenon
Gold
Platinum
Lead
Radon
Radium
Tungsten
Radium
Mercury
Osmium
Bismuth
Plutonium
Curium
Fermium
Fracium
'''

language = lorem_ipsum

def pairwise(iterable):
    """
    Yield pairs of consecutive elements in iterable.
    
    >>> list(pairwise('abcd'))
    [('a', 'b'), ('b', 'c'), ('c', 'd')]
    """
    iterator = iter(iterable)
    try:
        a = iterator.next()
    except StopIteration:
        return
    for b in iterator:
        yield a, b
        a = b


class MarkovChain(object):
    """
    If a system transits from a state to another and the next state depends
    only on the current state and not the past, it is said to be a Markov chain.
    
    It is determined by the probability of each next state from any current
    state.
    
    See http://en.wikipedia.org/wiki/Markov_chain
    
    The probabilities are built from the frequencies in the `sample` chain.
    Elements of the sample that are not a valid state are ignored.
    """
    def __init__(self, sample):
        self.counts = counts = defaultdict(lambda: defaultdict(int))
        for current, next in pairwise(sample):
            counts[current][next] += 1
        
        self.totals = dict(
            (current, sum(next_counts.itervalues()))
            for current, next_counts in counts.iteritems()
        )
        

    def next(self, state):
        """
        Choose at random and return a next state from a current state,
        according to the probabilities for this chain
        """
        nexts = self.counts[state].iteritems()
        # Like random.choice() but with a different weight for each element
        rand = random.randrange(0, self.totals[state])
        # Using bisection here could be faster, but simplicity prevailed.
        # (Also it’s not that slow with 26 states or so.)
        for next_state, weight in nexts:
            if rand < weight:
                return next_state
            rand -= weight
    
    def __iter__(self):
        """
        Return an infinite iterator of states.
        """
        state = random.choice(self.counts.keys())
        while True:
            state = self.next(state)
            yield state

chain_japanese = MarkovChain(
        c for c in language.lower() if c in string.ascii_lowercase
    )

chain_periodic = MarkovChain( periodic.lower() )

def main():
    chain = MarkovChain(
        c for c in japanese.lower() if c in string.ascii_lowercase
    )
    print ''.join(itertools.islice(chain, 5))

if __name__ == '__main__':
    main()
