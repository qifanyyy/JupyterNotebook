# diketahui tabel mahasiswa dan mata kuliah
# mhs	makul	mk1	mk2	mk3	mk4	mk5	mk6	mk7	mk8	mk9
# --------------------------------------------------
# mhs1		|	1		1		1		1		
# mhs2		|		1		1	1			1	
# mhs3		|	1	1		1			1			
# mhs4		|			1	1
# mhs5		|					1	1		1
# mhs6		|		1	1	
# mhs7		|	1					1
# mhs8		|		1							1
# mhs9		|				1					1
# mhs10		|					1			1	1
# mhs11		|		1		1	
# mhs12		|	1	1			1	
# mhs13		|		1		1			1	
# mhs14		|			1			1		1
# mhs15		|	1				1				1	
# mhs16		|	1	1		1	
# ==================================================
#				4	3	2	1	0	1	5	4	2
import numpy as np

n_makul = 118

# ubah ke dalam matriks adjacency (ketetanggaan)

#baca insidensi
def BuatInsidensi_Mhs_Makul(NamaFile, n_makul):
	data1dimensi = open(NamaFile).read().splitlines()

	data1dimensi = [ int(i) for i in data1dimensi ]
	pjg_data = len(data1dimensi)

	n_mhs = pjg_data/n_makul		# banyaknya mahasiswa dan dosen

	inc = np.array(data1dimensi).reshape((n_mhs, n_makul))
	return inc


inc = BuatInsidensi_Mhs_Makul("kode incidency.txt", n_makul)

#ubah insidensi ke adjacency matriks makul

#buat adjacency matrix
def BuatAdj(incidency_matriks, n_makul):
	adj = np.zeros((n_makul,n_makul), dtype=np.uint8)
	for baris in incidency_matriks:
		titik_hidup = [ i for i in range(n_makul) if baris[i] == 1 ]
		banyaknya_hidup = len(titik_hidup)
		if banyaknya_hidup > 1:
			for i in range(banyaknya_hidup - 1):
				for j in range(i+1, banyaknya_hidup):
					adj[titik_hidup[i], titik_hidup[j]] = 1
					adj[titik_hidup[j], titik_hidup[i]] = 1
	return adj

adj_tanpa_sks = BuatAdj(inc, n_makul)
adj_lama = np.copy(adj_tanpa_sks)
np.savetxt('adj_tanpa_sks.txt', adj_tanpa_sks, fmt='%d')
print adj_tanpa_sks[0:5,1]
#jangan sampai 2sks dan 3sks di satu slot yang sama
#buat sisi antara makul 2sks dengan yang 3sks
def sks2Adj(NamaFile_sks, n_makul, adjku):
	sks = open(NamaFile_sks).read().splitlines()
	sks = np.array([ int(i) for i in sks ])
	
	pilihan_sks = [2,3]
	dua_sks = np.array([i for i in range(n_makul) if sks[i] == 2])
	tiga_sks = np.array([i for i in range(n_makul) if sks[i] == 3])
	n_dua_sks = len(dua_sks)
	n_tiga_sks = len(tiga_sks)
	
	
	for i in range(n_dua_sks):
		for j in range(n_tiga_sks):
			adjku[dua_sks[i],tiga_sks[j]] = 1
			adjku[tiga_sks[j],dua_sks[i]] = 1
	adj = np.copy(adjku)
	return adj

adj = sks2Adj("sks.txt", 118, adj_lama)

np.savetxt('adjdgsks.txt', adj, fmt='%d')
#~ adj = adj_tanpa_sks

print adj[0:5,1]
print "apakah adj = adj tanpa sks?", np.all(adj_tanpa_sks == adj)
print "....."

#urutkan berdasarkan derajat tiap titiknya

def UrutAdj(adj, n_makul):
	# tambahkan derajat di baris dan kolom baru
	# buat matriks baru yang ukurannya menjadi lebih besar 1 baris dan 1 kolom
	adj_der = np.zeros((n_makul+1, n_makul+1), dtype=np.uint8)
	adj_der[:n_makul,:n_makul] = adj
	#~ print adj_der

	jml = adj.sum(axis=1)
	#~ print jml

	adj_der[:n_makul,n_makul] = jml
	adj_der[n_makul,:n_makul] = jml
	#~ print adj_der

	adj_tanda = np.zeros((n_makul+2, n_makul+2), dtype=np.uint8)
	adj_tanda[:n_makul+1,:n_makul+1] = adj_der
	#~ print adj_tanda
	adj_tanda[:n_makul,n_makul+1] = np.arange(n_makul)
	adj_tanda[n_makul+1,:n_makul] = np.arange(n_makul)
	#~ print adj_tanda

	print 'mengurutkan berdasarkan kolom ke:', n_makul
	urutan = adj_tanda[:n_makul,n_makul].argsort()[::-1]
	#~ print 'urutan:\n',urutan

	#urutkan baris2 berdasarkan kolom ke n_makul
	adj_urut = adj_tanda
	adj_urut[:n_makul,:n_makul+2] = adj_tanda[urutan]
	#~ print adj_urut

	#urutkan kolom2 berdasarkan baris ke n_makul
	adj_urut[:n_makul+2,:n_makul] = adj_tanda[:,urutan]
	#~ print adj_urut

	adj_baru = adj_urut[:n_makul,:n_makul]
	#~ print adj_baru
	
	return adj_baru, urutan

adj_baru_tanpa_sks, urutan = UrutAdj(adj_tanpa_sks, n_makul)
adj_baru, urutan = UrutAdj(adj, n_makul)

print np.all(adj_baru == adj_baru_tanpa_sks)

print adj_baru
print "-----------"
print adj_baru_tanpa_sks
#~ if adj_baru == adj_baru_tanpa_sks:
	#~ print "sama saja"
#~ else:
	#~ print "beda lho"

np.savetxt('adjbaru.txt', adj_baru, fmt="%d")
np.savetxt('adjbaru_tanpa_sks.txt', adj_baru_tanpa_sks, fmt="%d")
#~ simpanadj = open('adjbaru.txt','w')
#~ simpanadj.write(adj_baru)
#~ simpanadj.close

#~ simpanadj_tanpa_sks = open('adjbaru_tanpa_sks.txt','w')
#~ simpanadj_tanpa_sks.write(adj_baru_tanpa_sks)
#~ simpanadj_tanpa_sks.close

#########################################
#### ini tambahannya, bit warna graf muks
####-------------------------------------

def listkeint(list):
	b = ''
	for i in list:
		b += str(i)
	return int(b,2)

# Kita namakan dengan variabel "aint", yaitu matriks "adjacency"
## yang tiap barisnya diubah dari bit menjadi integer.
aint = [ listkeint(baris) for baris in adj_baru]
aint_tanpa_sks = [ listkeint(baris) for baris in adj_baru_tanpa_sks]

# Terus kita tampilkan deh..
#~ print "aint =", aint


pjgA = len(aint)
c = [ 0 for i in range(pjgA)]	#maks warna yang boleh adalah sebanyak pjgA
#~ print "c =", c

topeng = 1 << (pjgA - 1)

n_warna = 0
# Setelah menginisialisasi "topeng" nya,
# di bagian ini lah proses pewarnaan untuk seluruh grafnya
for i in range(pjgA): # untuk kolom di A
	
	#sudah lebih dari 14 warna belum?
	#kalau sudah, lepaskan ikatan antara 2sks dan 3sks
	for id, wc in enumerate(c):
		if wc != 0:
			n_warna = id
	if n_warna < 14:
		apakai = aint
	else:
		apakai = aint_tanpa_sks
	 
	
	for j in range(pjgA): # ini untuk baris di C
		cek = c[j] & topeng # bitnya hidup ndak ya?
		if cek == 0:
			c[j] = c[j] | apakai[i]
			topeng = topeng >> 1
			break




# Akhirnya bisa kita tampilkan di layar dengan script ini.
#~ print "Setelah kutunggu cukup lama, akhirnya ketemu juga.."
print "c =", c

# Itu kalau kita artikan di bahasa manusia seperti ini
print "\nItu artinya seperti ini:"

h = [ 1<<pjgA | i for i in c if i != 0]
h.append(1<<pjgA)
h_list = [ list(bin(i))[3:] for i in h ]
print h_list
print len(h_list)
print len(h_list[0])
hku = [ map(int,baris) for baris in h_list ]
h_array = np.array(hku)
print "panjang h_array: ",len(h_array)
print "lebar h_array: ",len(h_array[0])
print h_array
np.savetxt('h_array.txt', h_array, fmt = '%d')

permakul = np.zeros(118)	#[]
posisi = 0
for makul in range(pjgA):					#kolom
	for slotwaktu in range(len(h_array)):	#baris
		if h_array[slotwaktu,makul] == 0:
			permakul[posisi] = slotwaktu
			posisi += 1
			break

print len(permakul)
np_permakul = np.array(permakul)
print "permakul:\n", permakul
np.savetxt('permakul.txt', np_permakul, fmt="%d")

gabung = np.zeros((n_makul,2))
gabung[:,0] = urutan
gabung[:,1] = np_permakul

np.savetxt('gabung.txt', gabung, fmt="%d")

gabung_urut = gabung[gabung[:,0].argsort()]
np.savetxt('gabungurut.txt', gabung_urut, fmt="%d")


print urutan
warna = []
for baris in h_array:
	ini = []
	for i in xrange(n_makul):
		if baris[i] == 0:
			ini.append(urutan[i])
	warna.append(ini)

keluaran = open('keluaran.txt','w')
print warna
print 'Okay, jadi bisa menggunakan',len(warna),'warna saja'
keluaran.write('Okay, jadi bisa menggunakan %s warna saja\n' %(len(warna)))

i = 0
for baris in warna:
	print 'warna',i,'bisa untuk titik:',baris
	keluaran.write('warna %s bisa untuk titik: %s\n' %(i, baris))
	i = i + 1

keluaran.close()
#~ npwarna = np.asarray(warna)
#~ print npwarna
	#~ print [urut[i] for i in xrange(n_makul) if baris[i] == 0 ]
