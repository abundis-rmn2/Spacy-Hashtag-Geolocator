from multi_rake import Rake

text = (
    'Liberalismo estas politika filozofio aŭ mondrigardo konstruita en '
    'ideoj de libereco kaj egaleco. Liberaluloj apogas larĝan aron de '
    'vidpunktoj depende de sia kompreno de tiuj principoj, sed ĝenerale '
    'ili apogas ideojn kiel ekzemple liberaj kaj justaj elektoj, '
    'civitanrajtoj, gazetara libereco, religia libereco, libera komerco, '
    'kaj privata posedrajto. Liberalismo unue iĝis klara politika movado '
    'dum la Klerismo, kiam ĝi iĝis populara inter filozofoj kaj '
    'ekonomikistoj en la okcidenta mondo. Liberalismo malaprobis heredajn '
    'privilegiojn, ŝtatan religion, absolutan monarkion kaj la Didevena '
    'Rajto de Reĝoj. La filozofo John Locke de la 17-a jarcento ofte '
    'estas meritigita pro fondado de liberalismo kiel klara filozofia '
    'tradicio. Locke argumentis ke ĉiu homo havas naturon rekte al vivo, '
    'libereco kaj posedrajto kaj laŭ la socia '
    'kontrakto, registaroj ne rajtas malobservi tiujn rajtojn. '
    'Liberaluloj kontraŭbatalis tradician konservativismon kaj serĉis '
    'anstataŭigi absolutismon en registaroj per reprezenta demokratio kaj '
    'la jura hegemonio.'
)

rake = Rake(max_words_unknown_lang=3)

keywords = rake.apply(text, text_for_stopwords=other_text)

print(keywords)