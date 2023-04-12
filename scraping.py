from bs4 import BeautifulSoup

with open('xskt_HCM_200_ngay.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), "html.parser")

tables = soup.find_all(class_="result")
# print("Number of tables found:", len(tables))

with open('data.csv', 'w') as f:

    f.write("Thu,Ngay,G8,G7,G6,G5,G4,G3,G2,G1,DB,\n")
    for table in tables:
        info = table.findAll("b")[0].text

        f.write(info[10] + ',')
        f.write(info[-5:] + ',')

        for tr in table.findAll('tr'):

            for em in tr.findAll('em'):
                f.write(em.text + ',')

            for p in tr.findAll('p'):
                f.write(p.text + ',')

        f.write('\n')
