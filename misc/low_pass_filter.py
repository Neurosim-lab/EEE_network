import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt
import matplotlib.pyplot as plt
import batch_utils, batch_analysis

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    #y = lfilter(b, a, data)
    y = filtfilt(b, a, data)
    return y


# Filter requirements.
order = 6
fs = 5000 #30.0       # sample rate, Hz
cutoff = 10 #3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
plt.ion()
plt.figure()
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# # Demonstrate the use of the filter.
# # First make some data to be filtered.
# T = 5.0         # seconds
# n = int(T * fs) # total number of samples
# t = np.linspace(0, T, n, endpoint=False)
# # "Noisy" data.  We want to recover the 1.2 Hz signal from this.
# data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)

# Using our own experimental data
exptrace = 2 # Trace number to filter (0 to 9)
expdata = batch_utils.import_excel("/u/graham/projects/eee/data/srdjan_20171017/B_73_004.xlsx")
t = np.array(expdata.index.tolist())
data = np.array(expdata.iloc[:,trace].tolist())

# Using our own sim data
simtrace = 6 # Trace number to filter (0 to 9)
batchname = 'glutAmp'
params, data = batch_utils.load_batch(batchname)
simdata = batch_analysis.get_vtraces(params, data, cellID=0, section="soma", stable=50)
data = simdata['yarray'][simtrace, :]
t = simdata['xvector']

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()