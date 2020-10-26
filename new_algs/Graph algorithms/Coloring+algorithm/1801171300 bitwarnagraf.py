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

adj = BuatAdj(inc, n_makul)


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

adj_baru, urutan = UrutAdj(adj, n_makul)



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

# Terus kita tampilkan deh..
#~ print "aint =", aint


pjgA = len(aint)
c = [ 0 for i in range(pjgA)]
#~ print "c =", c

topeng = 1 << (pjgA - 1)


# Setelah menginisialisasi "topeng" nya,
# di bagian ini lah proses pewarnaan untuk seluruh grafnya
for i in range(pjgA): # untuk kolom di A
	for j in range(pjgA): # ini untuk baris di C
		cek = c[j] & topeng # bitnya hidup ndak ya?
		if cek == 0:
			c[j] = c[j] | aint[i]
			topeng = topeng >> 1
			break

# Akhirnya bisa kita tampilkan di layar dengan script ini.
#~ print "Setelah kutunggu cukup lama, akhirnya ketemu juga.."
#~ print "c =", c

# Itu kalau kita artikan di bahasa manusia seperti ini
print "\nItu artinya seperti ini:"

h = [ 1<<pjgA | i for i in c if i != 0]
h_list = [ list(bin(i))[3:] for i in h ]
hku = [ map(int,baris) for baris in h_list ]
h_array = np.array(hku)
print h_array

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
