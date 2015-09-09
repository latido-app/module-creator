from music21 import *
import xml.dom.minidom as xml
import glob

libnameinput = raw_input('Full module name: ')
keyinput = raw_input('Module key? (8 chars): ')[:8]
doimages = raw_input("Do you need to create the images? (Y/N): ")
isrhythm = raw_input("Are these all rhythmic exercises? (Y/N): ")

if doimages == 'Y' or doimages == 'y':
    for fname in sorted(glob.glob('*.xml')):
        try:
            test = converter.parse(fname)
            sopr = test.parts[0]
            sopr.write('lily.png', 'image/'+fname[:-4])
            print 'succeeded: '+fname
        except:
            print "failed: "+fname

def calculate_countin (mfile):
    timesig = mfile.flat.getElementsByClass(meter.TimeSignature)
    beats = 0
    if 1 == len(timesig):
        beats = timesig[0].numerator
        countin = beats
    else:
        beats = timesig[1].numerator
        countin = beats - timesig[0].numerator
    if beats > 3 and beats % 3 == 0:
        beats = beats / 3.0
        countin = countin / 3.0
    if countin <= 1:
        countin = countin + beats
    return countin

doc = xml.Document()
latido = doc.createElement("latido")
xmlname = doc.createElement("name")
modulekey = doc.createElement("modulekey")
xmlimage = doc.createElement("imageextension")
xmlmidi = doc.createElement("midiextension")
xmlprogress = doc.createElement("progress")
doc.appendChild(latido)
latido.appendChild(xmlname)
latido.appendChild(modulekey)
latido.appendChild(xmlimage)
latido.appendChild(xmlmidi)
latido.appendChild(xmlprogress)
xmlname.appendChild(doc.createTextNode(libnameinput))
modulekey.appendChild(doc.createTextNode(keyinput))
xmlimage.appendChild(doc.createTextNode("png"))
xmlmidi.appendChild(doc.createTextNode("mid"))
for midifile in sorted(glob.glob('midi/*.mid')):
    xmlexercise = doc.createElement('exercise')
    xmlexercise.setAttribute('name',midifile[5:-4])
    xmlexercise.setAttribute('tempo','120')
    if isrhythm == 'Y' or isrhythm == 'y':
        xmlexercise.setAttribute('rhythm','true')
    temp = converter.parse(midifile)
    countin = calculate_countin(temp)
    xmlexercise.setAttribute('countin',str(countin))
    xmlprogress.appendChild(xmlexercise)
fn = keyinput + '.xml'
doc.writexml( open(fn, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
doc.unlink()
