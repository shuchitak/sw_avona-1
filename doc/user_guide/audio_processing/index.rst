################
Audio Processing
################

At the core of the Avona Reference Design are high-performance audio processing algorithms.  The algorithms are connected in a pipeline that takes its input from a pair of the microphone and executes a series of signal processing algorithms to extract a voice signal from a complex soundscape. The audio pipeline can accept a reference signal from a host system which is used to perform Acoustic Echo Cancellation (AEC) to remove audio being played by the host. The audio pipeline provides two different output channels - one that is optimized for Automatic Speech Recognition systems and the other for voice communications.

A flexible audio signal routing infrastructure and a range of digital inputs and outputs enables the Avona Reference Design to be integrated into a wide range of system configurations, that can be configured at start up and during operation through a set of control registers.  In addition, all source code is provided to allow for full customization or the addition of other audio processing algorithms.

AUDIO FEATURES
.. toctree:: 
   :maxdepth: 2

   ../../../modules/lib_aec/doc/index
