
from docx import Document
import roner


ner = roner.NER(named_persons_only= True,use_gpu= True,batch_size= 6,num_workers=4)


input_doc = Document(r"C:\Users\Tudor\Desktop\aaa.docx")

content = ["\n".join(p.text for p in input_doc.paragraphs)]

print("Content list created!")

# input_texts = ["În anul 2000 vedea lumina tiparului una dintre cele mai longevive reviste de istorie din acest colţ de ţară, Columna 2000, editată de Şcoala cu clasele I-VIII nr. 23 Timişoara şi ,,deschisă românilor de pretutindeni”, care va deveni, destul de rapid, una dintre revistele de referinţă, pe profil istoric, dar şi cu valenţe interdisciplinare, ale Banatului şi, implicit, ale României. Columna 2000 a fost gândită, încă de la bun început, ca o revistă bianuală şi, în egală măsură, ca o veritabilă tribună a românismului. Relevante, în acest sens, sunt cele două coperţi ale numerelor 1-2 (ianuarie-iunie 2000), pe coperta din faţă fiind postată imaginea Columnei lui Traian, aflată la Roma, şi cel mai cunoscut portret al domnitorului Mihai Viteazul, primul ,,unificator de ţară”, alături de un citat al savantului Nicolae Iorga, care evidenţiază rolul determinant al acestuia din urmă în împlinirea visului secular de unire a tuturor românilor într-un singur stat: ,,După 1600 niciun român   n-a mai putut gândi unirea fără uriaşa lui personalitate, fără paloşul sau securea lui ridicată spre cerul dreptăţii, fără chipul lui de o curată şi desăvârşită poezie tragică...”. Coperta din spate este dominată de portretul lui Vlad Ţepeş, cele trei domnii ale acestuia reprezentând o pledoarie pentru perpetuarea valorilor morale în societatea românească, completat, în mod firesc, de observaţiile cronicarului Laonic Chalcocondil: ,,...chiar şi împăratul (Mahomed al II-lea), cuprins de uimire, spunea întruna că nu poate să ia ţara unui bărbat care face lucruri aşa mari (Vlad Ţepeş – n.n.) şi, mai presus de fire, ştie să se folosească aşa de domnia şi de supuşii lui. Mai spunea că acest bărbat, care face astfel de isprăvi, ar fi vrednic de mai mult”. Numărul dublu 1-2 (2000) al revistei analizate cuprindea un număr relativ redus de pagini (20), însă calitatea materialelor publicate era net superioară unei simple reviste şcolare, acesta fiind, fără îndoială, meritul exclusiv al colectivului de redacţie, alcătuit din: redactor-şef – prof. Tiberiu Ciobanu (care îşi va pune, de altfel, amprenta asupra revistei, de-a lungul timpului, girând calitatea articolelor şi caracterul său interdisciplinar, din ce în ce mai accentuat); secretar de redacţie – prof. Monica-Minodora Păcurariu; secretar adjunct de redacţie – Raluca Neiconi, elevă în clasa a VI-a A; redactori – prof. Rodica Corbeanu, înv. Titus Drăgan, înv. Codruţa Bontilă, Florentina Bîscă – clasa a VI-a B, Alexandru Stînean – clasa a V-a şi Vlad Crişan – clasa a V-a; tehnoredactare computerizată – Valentin Manolescu; consultant redacţional – Aurel Turcuş. Se constată implicarea firească a elevilor merituoşi în ,,construirea” unei reviste şcolare de anvergură şi cooptarea, în colectivul de redacţie, a renumitului om de cultură Aurel Turcuş, care va deveni "]

output_texts = ner(content)

print("NER done!")

name_list = []

for output_text in output_texts:
    for word in output_text['words']:
        if word['tag'] == 'PERSON':
            if word['multi_word_entity'] == False:
                name_list.append(word['text'])
            else:
                name_list[-1] = name_list[-1] + ' ' + word['text']


# for index ,name in enumerate(name_list):
#     print(f"{index+1}.{name}")

print("Filtering done!")

output_doc = Document()
for index ,name in enumerate(name_list):
    output_doc.add_paragraph(f"{index+1}.{name}")

print("Output file created!")
output_doc.save(r"C:\Users\Tudor\Desktop\output.docx")

print("Export done!")
