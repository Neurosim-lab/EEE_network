import matplotlib.pyplot as plt
import os
import json
import numpy as np
import matplotlib.lines as mlines
import matplotlib.cm as cm
import random
import pandas as pd
import pickle
from pprint import pprint
import batch_analysis as ba


net_labels= ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PT5_5','PT5_6','PT5_7','PT5_8','PT5_9','PT5_10']
net_labels2= ['1', '2', '3', '4', '5','6','7','8','9','10']
pos_labels=[]

stats = ['spike_sync_profile', 'spike_profile', 'isi_profile']
#mats = ["ISI-distance", "SPIKE-distance", "SPIKE-Sync"]
mats = ['SPIKE-Sync']

gids = [] 
for k in range(len(net_labels)*2): 
	gids.append(range(200+((k)*40),200+((k)*40)+40))
#print gids

def list_data():
	global data_files		
	files = os.listdir(path)
	data_files = []
	
	for file in files:
		if file[-5:] == '.json':
			if not file[-8:] == 'cfg.json':
		 		if not file[-10:] == 'batch.json':
					#print file[:-5]
					data_files.append(file[:-5])
	
	return data_files		
	
def load_data(n=[0]):
	
	list_data()
	for i in range(len(n)):
		print 'Data included: '+str(data_files[n[i]])
	print 'loading data ...'

	global d	
	d={}
	for i,v in enumerate(data_files):
		if i in n:
			with open(path+data_files[i]+'.json') as json_data:
		    		d[v] = json.load(json_data) 
		else:
			pass    		    		 
	#print d
	print "Finished loading data"
	return d, data_files

def load_json(filename=None):
	global d
	with open(path+filename+".json") as json_data:
		d = json.load(json_data)
	return d 

def volt(network=[0]):
	#print network	
	load_data(n=network)
	
	global  time, v_soma, v_dend, v_apical
	v_soma = {}
	v_dend = {}
	v_apical ={}

	for f,p in enumerate(data_files):
		if f in network:
			time = d[p]['simData']['t']
			v_soma[f] = d[p]['simData']['v_soma']
			v_dend[f] = d[p]['simData']['v_basal']
			v_apical[f] = d[p]['simData']['v_apical']
		else:
			pass 
	return time, v_soma, v_dend, v_apical, data_files
		

def sync_test():
	import pyspike

	spkt_train = []

	empty_train = [[] for i in range(801)]

	for i in range(len(empty_train)):
		if i < 200:
			empty_train[i] = random.sample(xrange(0,1500), 0)
			spkt_train.append(pyspike.SpikeTrain(empty_train[i], timeRange))
		elif (i>=200 and i<400): 	
			empty_train[i] = random.sample(xrange(0,1500), 1)
			spkt_train.append(pyspike.SpikeTrain(empty_train[i], timeRange))
		elif (i>=400 and i<600): 	
			empty_train[i] = random.sample(xrange(0,1500), 5)
			spkt_train.append(pyspike.SpikeTrain(empty_train[i], timeRange))	
		elif i >= 600:
			empty_train[i] = random.sample(xrange(0,1500), 50)
			spkt_train.append(pyspike.SpikeTrain(empty_train[i], timeRange))			

	spike_sync = pyspike.spike_sync_matrix(spkt_train)

	for i in range(len(spkt_train)): 
		if i < 400:
			for v in range(400): 
				empty_array[i][v] = 1.0

	getmat['2'] = spike_sync-empty_array

def get_matrix(select='subset', min_spike_number=0, save=None, analysis=['SPIKE-Sync'], network= [0]):
	import pyspike

	load_data(network)

	getmat = {}
		
	empty_dict_array = {}
	no_empty_dict_array = {}

	spkts = {}
	spkinds = {}
	spktsRange = {}
	spkt_train ={}
	spike_sync ={}

	for f,p in enumerate(data_files):
		if f in network:
			spkts[f] = d[p]['simData']['spkt'] #list
			spkinds[f] = d[p]['simData']['spkid'] #list

			print 'Starting analysis of spike times per '+str(select)+': '+str(p)

			for t,y in enumerate(timeRange):

				spktsRange = [spkt for spkt in spkts[f] if timeRange[t][0] <= spkt <= timeRange[t][1]]
				
				spkt_train[str(f)+str(t)] =[]

				if select == 'subset':
					print 'Time Range: '+str(y)

					empty_array = np.zeros(((len(net_labels)*2),(len(net_labels)*2)))
					no_empty_array = np.zeros(((len(net_labels)*2),(len(net_labels)*2)))
					array_ii = np.zeros(((len(net_labels)*2),(len(net_labels)*2)))


					empty_gids=[]
					gids_included =[]

					for k,v in enumerate(gids):
							train =[]
							for i,gid in enumerate(v):
								for spkind,spkt in zip(spkinds[f],spkts[f]):
									if (spkind==gid and spkt in spktsRange): 
										train.append(spkt)

							spkt_train[str(f)+str(t)].append(pyspike.SpikeTrain(train, timeRange[t]))

							if len(train)<min_spike_number:
								empty_gids.append(k)
							else:
								gids_included.append(k)

					for i in range(len(spkt_train[str(f)+str(t)])): 
						if i in gids_included:
							for k,v in enumerate(gids_included): 
								no_empty_array[i][v] = 1.0

					for l in range(len(array_ii)):
						array_ii[l][l] = 1.0 	
					
					no_empty_dict_array[str(f)+str(t)] = no_empty_array


				elif select == 'cell':			
					
					print 'Time Range: '+str(y)

					empty_array = np.zeros(((len(net_labels)*80),(len(net_labels)*80)))
					no_empty_array = np.zeros(((len(net_labels)*80),(len(net_labels)*80)))

					empty_gids=[]
					spkmat2 = [] 
					gids_included =[]
					#sync = np.zeros(((len(net_labels)*80),(len(net_labels)*80)))

					for ii, subset in enumerate(gids):		
							spkmat = [pyspike.SpikeTrain([spkt for spkind,spkt in zip(spkinds[f],spkts[f]) if (spkind==gid and spkt in spktsRange)], timeRange[t]) for gid in set(subset)]
							spkt_train[str(f)+str(t)].extend(spkmat)

							for gid in set(subset):
								list_spkt=[spkt for spkind,spkt in zip(spkinds[f],spkts[f]) if (spkind==gid and spkt in spktsRange)]
								
								if len(list_spkt)<min_spike_number:
									empty_gids.append(gid)
								else:
									spkmat2.append(pyspike.SpikeTrain(list_spkt, timeRange[t]))
									gids_included.append(gid)
							pos_labels.append(len(gids_included))
					
					#print gids_included
					empty_gids[:] = [x - 200 for x in empty_gids]
					gids_included[:]= [x - 200 for x in gids_included]
					#print empty_gids
					for i in range(len(spkt_train[str(f)+str(t)])): 
						if i in empty_gids:
							for k,v in enumerate(empty_gids): 
								empty_array[i][v] = 1.0
					
					for i in range(len(spkt_train[str(f)+str(t)])): 
						if i in gids_included:
							for k,v in enumerate(gids_included): 
								no_empty_array[i][v] = 1.0

					#print empty_array
					empty_dict_array[str(f)+str(t)] = empty_array
					no_empty_dict_array[str(f)+str(t)] = no_empty_array
				#print spkt_train
				for l,mat in enumerate(mats): 
						#spike_sync
						if (mat == 'ISI-distance' and mat in analysis):
								print str(mat)+", number of trains: "+ str(len(spkt_train[str(f)+str(t)]))
								isi_distance = pyspike.isi_distance_matrix(spkt_train[str(f)+str(t)])							
								getmat[str(f)+str(t)+str(l)] =  isi_distance
								
						elif (mat in analysis and mat=='SPIKE-distance'):
								print str(mat)+", number of trains: "+ str(len(spkt_train[str(f)+str(t)]))
								spike_distance = pyspike.spike_distance_matrix(spkt_train[str(f)+str(t)])							
								getmat[str(f)+str(t)+str(l)] =  spike_distance
								
						elif (mat in analysis and  mat =='SPIKE-Sync'):
								print str(mat)+", number of trains: "+ str(len(spkt_train[str(f)+str(t)]))
								spike_sync[str(f)+str(t)] = pyspike.spike_sync_matrix(spkt_train[str(f)+str(t)])							
								#if select == 'subset':
								getmat[str(f)+str(t)+str(l)] = (spike_sync[str(f)+str(t)] * no_empty_dict_array[str(f)+str(t)]) + array_ii
								#elif select == 'cell':
								#getmat[str(f)+str(t)+str(l)] = spike_sync[str(f)+str(t)] * no_empty_dict_array[str(f)+str(t)]

				empty_array = np.zeros(((len(net_labels)*80),(len(net_labels)*80)))
		else: 
			pass

	
	if save == True:		
		with open(str(path)+'data1.pkl', 'wb') as output:
			pickle.dump(getmat, output)		

	return getmat
	print 'finished getting data for matrix plotting'

def get_json():
	with open('data.json') as json_data:
		    d = json.load(json_data)
	return d   

def get_pickle(filename=None):
	global getmat
	with open(str(path)+str(filename)+".pkl", "rb") as fp:
    		getmat = pickle.load(fp)
	return getmat

def rate(network =[7], type_rate = ['overall','inst'], save=False):
	import pyspike
	global rate_dict

	load_data(network)	
	print 'Starting analysis of rate...'
	
	spkts = {}
	spkinds = {}
	spktsRange = {}
	spkt_train = {}	
	rate_dict = {'overall': {}, 'inst':{}}

	for f,p in enumerate(data_files):
		if f in network:
			spkts[f] = d[p]['simData']['spkt'] #list
			spkinds[f] = d[p]['simData']['spkid'] #list

			for t,y in enumerate(timeRange):

				print 'Time Range: '+str(y)
				rate_mat_all = [[] for i in range(len(net_labels)*2)]
				rate_mat_inst = [[] for i in range(len(net_labels)*2)]
				timeRange_s = (timeRange[t][1]-timeRange[t][0])/1000.0

				spktsRange = [spkt for spkt in spkts[f] if timeRange[t][0] <= spkt <= timeRange[t][1]]
				
				for w in type_rate: 
					for ii, subset in enumerate(gids):									
						for gid in set(subset):														
							list_spkt=[spkt for spkind,spkt in zip(spkinds[f],spkts[f]) if (spkind==gid and spkt in spktsRange)]
							
							if w =='overall':
								gid_rate = float(len(list_spkt))/timeRange_s 
							elif w =='inst':	
								if len(list_spkt)<=1:
									pass 
								else:
									for x in range(len(list_spkt)):																 
										if not x==(len(list_spkt)-1):
											spkt_inst_rate = 1000.0/(list_spkt[x+1]-list_spkt[x]) 
											rate_mat_inst[ii].append(spkt_inst_rate)
				
				
				rate_dict['overall'][str(p)+'_'+str(t)] = rate_mat_all
				rate_dict['inst'][str(p)+'_'+str(t)] = rate_mat_inst
	#print rate_dict
	if save == True:		
		with open(str(path)+'rate.pkl', 'wb') as output:
			pickle.dump(rate_dict, output)		

	print 'finished getting rate analysis'
	return rate_dict

def detectDepolBlock(volt, minSamples=200, vRange=[-50, -10]):
    cumm = 0
    for v in volt:
        if v >= vRange[0] and v<= vRange[1]:
            cumm += 1
            if cumm > minSamples:
                return 1
        else:
            cumm = 0

    return 0 


def list_all_dbs(f=None, p=None):
	#list_data()
    dbs = []
    for cell in cells[f]:
	    trace = d[p]['simData']['v_soma'][cell]
	    db = detectDepolBlock(trace)
	    if db == 1:
	        dbs.append(cell)   
    return dbs

def plat_analysis(network=[0], plot_depol=False, plot_plats = True, plot_non_plats =True, save=True):

	load_data(n=network)
	global cells, traces
	output_dir = path 

	data_plat ={}
	cells = {}
	traces = {}

	for f,p in enumerate(data_files):
		if f in network:			
			time = d[p]['simData']['t']
			cells[f] = d[p]['simData']['v_soma'].keys()
			traces[f] = [d[p]['simData']['v_soma'][cell] for cell in cells[f]]
			db_cells = list_all_dbs(f=f, p=p)         
			db_cells.sort()
	
			print
			print("Number of Depol Block cells: " + str(len(db_cells)))
			print("Depol block cells:")
			print(db_cells)

			if plot_depol:
			    for cell in db_cells:
			        trace = d[p]['simData']['v_soma'][cell]
			        fig = plt.figure()
			        plt.plot(trace)
			        plt.figtext(0.5, 0.80, "Depolarization Blockade", ha="center", fontweight="bold")
			        plt.ylabel("Membrane Potential (mv)")
			        plt.xlabel("Time (ms)")
			        plt.title(cell + " Depolarization Blockade")
			        plt.ylim([-80, 20])
			        fig.savefig(os.path.join(output_dir, "depol_block_" + cell))
			        plt.close(fig)

			good_cells = [cell for cell in cells[f] if cell not in db_cells]
			good_traces = [d[p]['simData']['v_soma'][cell] for cell in good_cells]

			plat_cells = range(0, 125)
			plat_cells.extend(range(250,375))
			plat_cells.extend(range(500,625))
			plat_cells.extend(range(750,875))
			plat_cells = ["cell_" + str(cell) for cell in plat_cells]

			non_plat_cells = range(125, 250)
			non_plat_cells.extend(range(375,500))
			non_plat_cells.extend(range(625,750))
			non_plat_cells.extend(range(875,1000))
			non_plat_cells = ["cell_" + str(cell) for cell in non_plat_cells]

			num_spikes = []
			plat_amps  = []
			plat_durs  = []
			spk_freqs  = []

			print
			print("Plateau Cells")
			print("=============")

			for cell in plat_cells:

			    print(cell)

			    num_spike = ba.meas_trace_num_spikes(d[p]['simData']['v_soma'][cell], showwork=False)
			    num_spikes.append(num_spike)
			    
			    plat_amp, plat_volt = ba.meas_trace_plat_amp(d[p]['simData']['v_soma'][cell], showwork=False)
			    plat_amps.append(plat_amp)

			    if plot_plats:
			        plat_dur, plat_time = ba.meas_trace_plat_dur(d[p]['simData']['v_soma'][cell], showwork=os.path.join(output_dir, "plat_durs_" + cell))
			    else:
			        plat_dur, plat_time = ba.meas_trace_plat_dur(d[p]['simData']['v_soma'][cell], showwork=False)
			    plat_durs.append(plat_dur)

			    spk_freq = ba.meas_trace_spike_freq(d[p]['simData']['v_soma'][cell])
			    spk_freqs.append(spk_freq)

			num_spikes_non_plat = []
			plat_amps_non_plat  = []
			plat_durs_non_plat  = []
			spk_freqs_non_plat  = []

			print
			print("Non-plateau cells")
			print("=================")
			print

			for cell in non_plat_cells:

			    print(cell)

			    num_spike = ba.meas_trace_num_spikes(d[p]['simData']['v_soma'][cell], showwork=False)
			    num_spikes_non_plat.append(num_spike)
			    
			    plat_amp, plat_volt = ba.meas_trace_plat_amp(d[p]['simData']['v_soma'][cell], showwork=False)
			    plat_amps_non_plat.append(plat_amp)

			    if plot_non_plats:
			        plat_dur, plat_time = ba.meas_trace_plat_dur(d[p]['simData']['v_soma'][cell], showwork=os.path.join(output_dir, "no_plat_plat_durs_" + cell))
			    else:
			        plat_dur, plat_time = ba.meas_trace_plat_dur(d[p]['simData']['v_soma'][cell], showwork=False)
			    plat_durs_non_plat.append(plat_dur)

			    spk_freq = ba.meas_trace_spike_freq(d[p]['simData']['v_soma'][cell])
			    spk_freqs_non_plat.append(spk_freq)

			data_plat[f] = {"num_spikes": num_spikes}
			data_plat[f]['plat_amps'] = plat_amps
			data_plat[f]['plat_durs'] = plat_durs
			data_plat[f]['spk_freqs'] = spk_freqs
			data_plat[f]['num_spikes_non_plat'] = num_spikes_non_plat
			data_plat[f]['plat_amps_non_plat'] = plat_amps_non_plat
			data_plat[f]['plat_durs_non_plat'] = plat_durs_non_plat
			data_plat[f]['spk_freqs_non_plat'] = spk_freqs_non_plat

	if save == True:		
		with open(str(path)+'data_plat.pkl', 'wb') as output:
			pickle.dump(data_plat, output)

	return data_plat
	print 'finished getting data for plateau analysis'	

def plot_hist(data=None, label=['Plats'], title=None, binwidth = 15, xlabel=None, xlim=[0,10], ylim = [0,0.5], save=None):
	
	
	hist_output_dir = path #os.path.split(output_dir)[0]

	fig = plt.figure()
	plt.hist(data, normed=True,bins=np.arange(min(data), max(data) + binwidth, binwidth), label=label)
	plt.xlim(xlim)
	plt.ylim(ylim)
	#plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel("Fraction of Cells")
	#plt.legend()
	fig.savefig(os.path.join(hist_output_dir, save))


def matrix_im(mat=None, ax=None, title=None, group = 'cell'):
	plot_params()
	global cax
	cmap =  cm.coolwarm #cm.jet #
	cax = ax.imshow(mat, interpolation='none', cmap=cmap, vmin=0.0, vmax=1.0)

	ax.set_title(title,fontsize=14)
	
	if group == 'cell':
		g=0.5
	elif group == 'subset':
		g = 0.25

	ax.set_yticks(np.arange(((len(mat)/(len(gids)/2.0))*(0.0+g)), len(mat), (len(mat)/(len(gids)/2.0))), minor=False)
	ax.set_yticks(np.arange(((len(mat)/(len(gids)/2.0))*(0.5+g)), len(mat), (len(mat)/(len(gids)/2.0))), minor=True)
	ax.yaxis.grid(True, which='minor')

	ax.set_xticks(np.arange(((len(mat)/(len(gids)/2.0))*(0.0+g)), len(mat), (len(mat)/(len(gids)/2.0))), minor=False)
	ax.set_xticks(np.arange(((len(mat)/(len(gids)/2.0))*(0.5+g)),len(mat), (len(mat)/(len(gids)/2.0))), minor=True)
	ax.grid(which='minor', color='w', linestyle='-', linewidth=0.5)

	ax.set_xticklabels(net_labels2,rotation='horizontal')
	ax.set_yticklabels(net_labels2,rotation='horizontal')
	return cax

def matrix_subplot(filename=None, network=None, savefig=None, group = 'cell'):
	
	get_pickle(filename)
	list_data()

	fig, (ax1,ax2,ax3) = plt.subplots(1,3, sharey = True, sharex = False, figsize = (12,4))

	matrix_im(getmat[str(network[0])+'10'],ax1, "2nd stim: 200 ms" , group)
	matrix_im(getmat[str(network[1])+'10'],ax2, "2nd stim: 300 ms", group)
	matrix_im(getmat[str(network[2])+'10'],ax3, "2nd stim: 400 ms" , group)

	#matrix_im(getmat[str(network)+'00'],ax1,  'Time range: '+str(timeRange[0][0])+'-'+str(timeRange[0][1])+' ms', group)
	#matrix_im(getmat[str(network)+'10'],ax2,  'Time range: '+str(timeRange[1][0])+'-'+str(timeRange[1][1])+' ms', group)
	#matrix_im(getmat[str(network)+'20'],ax3,  'Time range: '+str(timeRange[2][0])+'-'+str(timeRange[2][1])+' ms', group)

	fig.subplots_adjust(right=0.9, top=0.8)#, wspace= 0.15)
	cbar_ax = fig.add_axes([0.92, 0.1, 0.01, 0.7])
	fig.colorbar(cax, cax=cbar_ax)#, vmin=0.0)#, vmax=1.0)
	plt.suptitle('Sync in time range: '+str(timeRange[1][0])+'-'+str(timeRange[1][1])+' ms', fontsize=16)
	fig.savefig(str(out_path)+str(savefig)+'.png')
	#plt.show()

def boxplot_plot(data, ax=None, xlabel=None, xlim=[-2,30]):
	
	plot_params()
	colorList = plt.cm.Set3(np.linspace(0, 1, 20))
	meanpointprops = dict(marker=(5,1,0), markeredgecolor='black', markerfacecolor='white')
	labels= ['1_Plat','1_noStim','2_Plat','2_noStim','3_Plat','3_noStim','4_Plat','4_noStim','5_Plat','5_noStim','6_Plat','6_noStim','7_Plat','7_noStim','8_Plat','8_noStim','9_Plat','9_noStim','10_Plat','10_noStim']

	bp = ax.boxplot(data, labels=labels, meanprops=meanpointprops, widths=0.6, whis=1.5,showmeans=True, patch_artist=True, vert=False)#, labels=labels[::-1], meanprops=meanpointprops, whis=1.5, widths=0.6, vert=False, showmeans=True, patch_artist=True)
	ax.set_xlabel(xlabel, fontsize = 16)	
	ax.grid(axis='x', color="0.9", linestyle='-', linewidth=1)
	ax.invert_yaxis()
	ax.set_xlim(xlim)
	
	for i in range(0, len(bp['boxes'])):
	            bp['boxes'][i].set_facecolor(colorList[i])
	            bp['boxes'][i].set_linewidth(2)
	            bp['whiskers'][i*2].set_linewidth(2)
	            bp['whiskers'][i*2 +1].set_linewidth(2)
	            bp['medians'][i].set_linewidth(3)
	            bp['medians'][i].set_color('k')
	            for c in bp['caps']:
	                    c.set_color('k')
	                    c.set_linewidth(2)
	return bp
	
def boxplot_rate(filename=None, rate_type='inst', network=None, savefig=None, xlim=[-2,30]):

	rate(network=[network])
	#get_pickle(filename)
	list_data()

	fig, (ax1,ax2,ax3) = plt.subplots(1,3, sharey =True, figsize = (12,6))

	boxplot_plot(rate_dict[rate_type][str(data_files[network])+'_'+str(0)], ax1, str(timeRange[0][0])+'-'+str(timeRange[0][1])+' ms', xlim)# 
	boxplot_plot(rate_dict[rate_type][str(data_files[network])+'_'+str(1)], ax2, str(timeRange[1][0])+'-'+str(timeRange[1][1])+' ms', xlim)# 
	boxplot_plot(rate_dict[rate_type][str(data_files[network])+'_'+str(2)], ax3, str(timeRange[2][0])+'-'+str(timeRange[2][1])+' ms', xlim)# 
	#boxplot_plot(getmat[rate_type][str(data_files[network])+'_'+str(3)], ax4, str(timeRange[3][0])+'-'+str(timeRange[3][1])+' ms', xlim)# 

	#ax2.set_title(str(data_files[network]+", rate (Hz)"), fontsize=12)
	fig.subplots_adjust(wspace=0.1)
	plt.suptitle(str(data_files[network]+", rate (Hz)"), fontsize=16)
	plt.savefig(str(out_path)+str(data_files[network])+'_bprate.png')
	#plt.show()

def boxplot_sync(filename=None, network=None, savefig=None, xlim=[-0.1,2.0]):
	get_pickle(filename)
	list_data()

	cluster = []
	for i in range(0,40):
		cluster.extend(getmat['010'][i][:40])
	cluster.mean()
	#cluster.extend(getmat['010'][1][:40])

	print cluster

	#print getmat['010'][40:80]


	#fig, (ax1,ax2,ax3) = plt.subplots(1,3, sharey =True, figsize = (12,6))
	"""
	boxplot_plot(getmat[str(network)+str(0)+str(0)], ax1, str(timeRange[0][0])+'-'+str(timeRange[0][1])+' ms', xlim)# 
	boxplot_plot(getmat[str(network)+str(1)+str(0)], ax2, str(timeRange[1][0])+'-'+str(timeRange[1][1])+' ms', xlim)# 
	boxplot_plot(getmat[str(network)+str(2)+str(0)], ax3, str(timeRange[2][0])+'-'+str(timeRange[2][1])+' ms', xlim)# 

	fig.subplots_adjust(wspace=0.1)
	plt.suptitle(str(data_files[network]+", rate (Hz)"), fontsize=16)
	plt.savefig(str(out_path)+str(data_files[network])+'_bprate.png')
	plt.show()
	"""

	
def plot_mat(mat,group='cell',colormap='f',labels=net_labels,title=None,savefig=None):
	plot_params()
	print 'Plotting matrix '+str(title)
	
	fig, ax = plt.subplots()
	cmap = cm.jet
	cmap_r = cm.get_cmap('jet_r')
	
	if colormap == 'f':
		cax = ax.imshow(mat, interpolation='none', cmap=cmap, vmin=0.0, vmax=1.0)
	elif colormap == 'r':
		cax = ax.imshow(mat, interpolation='none', cmap=cmap_r)#, vmin=0.0, vmax=1.0)

	ax.set_title(title,fontsize=16)

	cbar = fig.colorbar(cax)

	if group == 'cell': 
		g=0.5
	elif group == 'subset':
		g=0.25	 
	
	minor_pos=[]
	major_pos=[]

	for i,v in enumerate(pos_labels):
		l = range(0,len(pos_labels),2)	
		if not i in l:
			minor_pos.append(v)
	
	for i in range(len(minor_pos)):
		if i == 0:
			major_pos.append((minor_pos[i])/2.0)
		else:	
			major_pos.append(minor_pos[i-1]+(minor_pos[i]-minor_pos[i-1])/2.0)


	if labels==net_labels:
	
		ax.set_yticks(np.arange(((len(mat)/(len(gids)/2.0))*(0.0+g)), len(mat), (len(mat)/(len(gids)/2.0))), minor=False)
		ax.set_yticks(np.arange(((len(mat)/(len(gids)/2.0))*(0.5+g)), len(mat), (len(mat)/(len(gids)/2.0))), minor=True)
		ax.yaxis.grid(True, which='minor')

		ax.set_xticks(np.arange(((len(mat)/(len(gids)/2.0))*(0.0+g)), len(mat), (len(mat)/(len(gids)/2.0))), minor=False)
		ax.set_xticks(np.arange(((len(mat)/(len(gids)/2.0))*(0.5+g)),len(mat), (len(mat)/(len(gids)/2.0))), minor=True)
		ax.grid(which='minor', color='w', linestyle='-', linewidth=0.5)

		ax.set_xticklabels(net_labels,rotation='vertical')
		ax.set_yticklabels(net_labels,rotation='horizontal')
	
	if labels=='no_empty':

		ax.set_yticks(minor_pos, minor=True)
		ax.set_yticks(major_pos, minor=False)
		ax.yaxis.grid(True, which='minor')

		ax.set_xticks(minor_pos, minor=True)
		ax.set_xticks(major_pos, minor=False)
		ax.grid(which='minor', color='w', linestyle='-', linewidth=0.5)
		
		ax.set_xticklabels(net_labels,rotation='horizontal')
		ax.set_yticklabels(net_labels,rotation='horizontal')
	

	plt.tight_layout()
	#fig.savefig(str(out_path)+str(group)+'_'+str(savefig))
	plt.show()

	
def get_data():
	
	print 'Starting analysis of spike times per cell: '+str(label_network)

	sync_data = [[[[]for i in range(2)] for x in range(len(gids))] for p in range(len(stats))]


	spktsRange = [spkt for spkt in spkts if timeRange[0] <= spkt <= timeRange[1]]

	for i,stat in enumerate(stats): 
		for ii, subset in enumerate(gids):		
			spkmat = [pyspike.SpikeTrain([spkt for spkind,spkt in zip(spkinds,spkts) if (spkind==gid and spkt in spktsRange)], timeRange) for gid in set(subset)]
			
			if stat=='spike_sync_profile':
				print str(stat)+", subset: "+str(ii)+", number of trains: "+str(len(spkmat))
				syncMat1 = pyspike.spike_sync_profile(spkmat)
				x, y = syncMat1.get_plottable_data()
				sync_data[i][ii][0] = x
				sync_data[i][ii][1] = y

			elif stat=='spike_profile':
				print str(stat)+", subset: "+str(ii)+", number of trains: "+str(len(spkmat))
				syncMat2 = pyspike.spike_profile(spkmat)
				x, y = syncMat2.get_plottable_data()
				sync_data[i][ii][0] = x
				sync_data[i][ii][1] = y

			elif stat=='isi_profile':
				print str(stat)+", subset: "+str(ii)+", number of trains: "+str(len(spkmat))
				syncMat3 = pyspike.isi_profile(spkmat)
				x, y = syncMat3.get_plottable_data()
				sync_data[i][ii][0] = x
				sync_data[i][ii][1] = y

def plot_params():
	params = {
	        'axes.labelsize': 14,
	        'font.size': 14,
	        'legend.fontsize': 14,
	        'xtick.labelsize': 12,
	        'ytick.labelsize': 12,
	        'text.usetex': False,
	        }

	plt.rcParams.update(params)

def plotSync(x=None, y=None, ax= None, label=None, color= 'black'):
	plot_params()
	plt = ax.plot(x, y, color = color, linestyle = 'solid', linewidth=1.0)
	ax.set_ylim(-80, 30)
	ax.set_yticks(np.arange(-80, 30, step = 20.0))
	#ax.set_xlim(-10, )
	#ax.set_title(label, fontsize=12, loc = 'right') 
	#ax.set_title(label, fontsize=12) 
	#ax.text(.85,.8,label,horizontalalignment='center',transform=ax.transAxes)

def matrixplot(x=None, title=None, savefig=None):

	fig,((ax1,ax6),(ax2,ax7),(ax3,ax8),(ax4,ax9),(ax5,ax10)) = plt.subplots(5,2, sharey = True, sharex = True, figsize = (8,9))

	plotSync(sync_data[x][0][0],sync_data[x][0][1], ax1, net_labels[0], 'red') 
	plotSync(sync_data[x][1][0],sync_data[x][1][1], ax1, net_labels[0], 'black') 

	plotSync(sync_data[x][2][0],sync_data[x][2][1], ax2, net_labels[1], 'red') 
	plotSync(sync_data[x][3][0],sync_data[x][3][1], ax2, net_labels[1], 'black') 

	plotSync(sync_data[x][4][0],sync_data[x][4][1], ax3, net_labels[2], 'red') 
	plotSync(sync_data[x][5][0],sync_data[x][5][1], ax3, net_labels[2], 'black') 

	plotSync(sync_data[x][6][0],sync_data[x][6][1], ax4, net_labels[3], 'red') 
	plotSync(sync_data[x][7][0],sync_data[x][7][1], ax4, net_labels[3], 'black') 

	plotSync(sync_data[x][8][0],sync_data[x][8][1], ax5, net_labels[4], 'red') 
	plotSync(sync_data[x][9][0],sync_data[x][9][1], ax5, net_labels[4], 'black') 

	plotSync(sync_data[x][10][0],sync_data[x][10][1], ax6, net_labels[5], 'red') 
	plotSync(sync_data[x][11][0],sync_data[x][11][1], ax6, net_labels[5], 'black') 

	plotSync(sync_data[x][12][0],sync_data[x][12][1], ax7, net_labels[6], 'red') 
	plotSync(sync_data[x][13][0],sync_data[x][13][1], ax7, net_labels[6], 'black') 

	plotSync(sync_data[x][14][0],sync_data[x][14][1], ax8, net_labels[7], 'red') 
	plotSync(sync_data[x][15][0],sync_data[x][15][1], ax8, net_labels[7], 'black') 

	plotSync(sync_data[x][16][0],sync_data[x][16][1], ax9, net_labels[8], 'red') 
	plotSync(sync_data[x][17][0],sync_data[x][17][1], ax9, net_labels[8], 'black') 

	plotSync(sync_data[x][18][0],sync_data[x][18][1], ax10, net_labels[9], 'red') 
	plotSync(sync_data[x][19][0],sync_data[x][19][1], ax10, net_labels[9], 'black') 


	ax3.set_ylabel('Synchronization', fontsize = 16)
	ax5.set_xlabel('Time (ms)', fontsize = 16)
	ax10.set_xlabel('Time (ms)', fontsize = 16)

	fig.suptitle(title, fontsize = 16) 
	black_line = mlines.Line2D([], [], color='black', label='No plateau')
	red_line = mlines.Line2D([], [], color='red', label='plateau')
	fig.legend(handles=[black_line,red_line], labels=['No plateau', 'Plateau'], loc='upper right')

	fig.subplots_adjust(hspace=0.4, wspace=0.05)
	plt.savefig(str(out_path)+str(savefig))
	plt.show()

def volt_plot_trace(x=None, net=None,title=None, savefig=None):
	volt(network=[net])

	print "Plotting voltage traces..."

	cellgid = []
	for  i in range(10): cellgid.append('cell_'+str((i*80)+205))

	fig,ax1 = plt.subplots(1,1, sharey = True, sharex = True, figsize = (9,6))

	plotSync(time, v_dend[net][cellgid[0]], ax1, net_labels[0], 'red') 
	plotSync(time, v_apical[net][cellgid[0]], ax1, net_labels[0], 'blue') 
	plotSync(time, v_soma[net][cellgid[0]], ax1, net_labels[0], 'black') 

	ax1.set_ylabel('Representative traces (mV)', fontsize = 16)
	ax1.set_xlabel('Time (ms)', fontsize = 16)
	#ax10.set_xlabel('Time (ms)', fontsize = 16)

	#fig.suptitle(title, fontsize = 16) 
	black_line = mlines.Line2D([], [], color='black', label='Soma')
	red_line = mlines.Line2D([], [], color='red', label='Basal Dendrite')
	blue_line= mlines.Line2D([], [], color='blue', label='Apical Dendrite')
	fig.legend(handles=[black_line,red_line,blue_line], labels=['Soma', 'Basal Dendrite', 'Apical Dendrite'], loc='upper right')

	#fig.subplots_adjust(hspace=0.1, wspace=0.05)
	plt.savefig(str(out_path)+str(savefig))

def volt_plot(x=None, net=None,title=None, savefig=None):

	volt(network=[net])

	print "Plotting voltage traces..."

	cellgid = []
	for  i in range(10): cellgid.append('cell_'+str((i*80)+205))

	fig,((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8),(ax9,ax10)) = plt.subplots(5,2, sharey = True, sharex = True, figsize = (8,9))

	plotSync(time, v_dend[net][cellgid[0]], ax1, net_labels[0], 'red') 
	plotSync(time, v_soma[net][cellgid[0]], ax1, net_labels[0], 'black') 
	
	plotSync(time, v_dend[net][cellgid[1]], ax2, net_labels[1], 'red')
	plotSync(time, v_soma[net][cellgid[1]], ax2, net_labels[1], 'black') 
	 
	plotSync(time, v_dend[net][cellgid[2]], ax3, net_labels[2], 'red')
	plotSync(time, v_soma[net][cellgid[2]], ax3, net_labels[2], 'black') 
	 
	plotSync(time, v_dend[net][cellgid[3]], ax4, net_labels[3], 'red')
	plotSync(time, v_soma[net][cellgid[3]], ax4, net_labels[3], 'black') 
	 
	plotSync(time, v_dend[net][cellgid[4]], ax5, net_labels[4], 'red')
	plotSync(time, v_soma[net][cellgid[4]], ax5, net_labels[4], 'black') 
	 
	plotSync(time, v_dend[net][cellgid[5]], ax6, net_labels[5], 'red')
	plotSync(time, v_soma[net][cellgid[5]], ax6, net_labels[5], 'black') 
	 
	plotSync(time, v_dend[net][cellgid[6]], ax7, net_labels[6], 'red') 
	plotSync(time, v_soma[net][cellgid[6]], ax7, net_labels[6], 'black') 
	
	plotSync(time, v_dend[net][cellgid[7]], ax8, net_labels[7], 'red')
	plotSync(time, v_soma[net][cellgid[7]], ax8, net_labels[7], 'black') 
	 
	plotSync(time, v_dend[net][cellgid[8]], ax9, net_labels[8], 'red')
	plotSync(time, v_soma[net][cellgid[8]], ax9, net_labels[8], 'black') 
	 
	plotSync(time, v_dend[net][cellgid[9]], ax10, net_labels[9], 'red')
	plotSync(time, v_soma[net][cellgid[9]], ax10, net_labels[9], 'black') 
	 

	ax5.set_ylabel('Representative traces (mV)', fontsize = 16)
	ax9.set_xlabel('Time (ms)', fontsize = 16)
	ax10.set_xlabel('Time (ms)', fontsize = 16)

	#fig.suptitle(title, fontsize = 16) 
	black_line = mlines.Line2D([], [], color='black', label='Soma')
	red_line = mlines.Line2D([], [], color='red', label='Basal Dendrite')
	fig.legend(handles=[black_line,red_line], labels=['Soma', 'Basal Dendrite'], loc='upper right')

	fig.subplots_adjust(hspace=0.1, wspace=0.05)
	plt.savefig(str(out_path)+str(savefig))
	#plt.show()

### bigger func

def plot_nets():
	group = ['cell','subset']
	list_data()
	sims = range(len(data_files))
	#sims = range(len(data_files)-1,len(data_files))

	#for i in sims:	 	
	#	volt_plot(title=str(data_files[i]), net = i, savefig = 'traces_'+str(data_files[i]))

	for i in sims:	 	
		volt_plot_trace(title=str(data_files[i]), net = i, savefig = 'traces_'+str(data_files[i]))


def check_netpyne():
	load_data(n=[0])
	print 'netpyne version: '+str(d[data_files[0]]['netpyne_version'])
	print 'netpyne changeset: '+str(d[data_files[0]]['netpyne_changeset'])
	print 'simConfig: '+str(d[data_files[0]]['simConfig'])

def plot_rate_nets():
	group = ['cell','subset']
	list_data()
	#sims = range(len(data_files))
	sims = range(len(data_files)-1,len(data_files))	
	for i in sims:
		rate(network=[i])
		boxplot_rate(str(path)+'rate',rate_type='overall', network = i, xlim = [-2,40])

def plot_plat_analysis():
	list_data()
	#ims = range(len(data_files))
	#sims = range(len(data_files)-2,len(data_files))
	sims =[0]
	plat_analysis(network=sims)

def plot_plat():

	get_pickle('data_plat')
	list_data()
	#sims = range(len(data_files)-2,len(data_files))
	sims = [0]
	for i in sims:
		plot_hist(data=getmat[i]['num_spikes'],title=data_files[i],xlabel='Number of Spikes',binwidth = 1,xlim=[0,20],ylim=[0,0.6], save = "hist_numspikes_"+data_files[i]+".png")
		plot_hist(data=getmat[i]['plat_amps'],title=data_files[i],xlabel='Plateau Amplitude (mV)',binwidth = 1,xlim=[0,30],ylim=[0,0.5], save = "hist_platamps_"+data_files[i]+".png")
		plot_hist(data=getmat[i]['plat_durs'],title=data_files[i],xlabel='Plateau Duration (ms)',binwidth = 10,xlim=[0,500],ylim=[0,0.04], save = "hist_platdurs_"+data_files[i]+".png")
		plot_hist(data=getmat[i]['spk_freqs'],title=data_files[i],xlabel='Frequency (Hz)',binwidth = 2,xlim=[0,80],ylim=[0,0.4], save = "hist_spkfreqs_"+data_files[i]+".png")

def sync_mat_plot():
	#sync_test()
	list_data()
	get_matrix('subset',2, True, network=[0,1,2])#[0,1,2,3,4,5,6,7,8,9]) #select data by individual spike train "cell" or grouped by subset "subset" 
	matrix_subplot(str(path)+'data1', network = [0,1,2], savefig = 'stimApical_sync', group = 'subset')


	#matrix_subplot(str(path)+'data1', network = 0, savefig = str(data_files[0])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 1, savefig = str(data_files[1])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 2, savefig = str(data_files[2])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 3, savefig = str(data_files[3])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 4, savefig = str(data_files[4])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 5, savefig = str(data_files[5])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 6, savefig = str(data_files[6])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 7, savefig = str(data_files[7])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 8, savefig = str(data_files[8])+'_sync', group = 'subset')
	#matrix_subplot(str(path)+'data1', network = 9, savefig = str(data_files[9])+'_sync', group = 'subset')


if __name__ == '__main__':

	path = '../../data/v45/'
	#path = 'batch_data/multi_params4/'

	out_path = path 

	timeRange = [[0, 200], [200, 500], [500,600]]
	#timeRange = [[200, 500]]

	#plot_nets()
	#plot_plat_analysis()
	#plot_plat()
	sync_mat_plot()
	
	#load_json("network162")
	#print d.simData

	#print d['params']
	#print d['data']['_0_2_2_1_1_1'].keys()

	
	