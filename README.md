# Speech To Text Converter (English)

## Table of Contents

-   [Introduction](#intro)
-   [Dockerized Repository](#docker)
-   [Requirements and installation](#requirements-and-installation)
-   [Server](#server)
-   [Client](#client)
-   [Roadmap](#roadmap)
-   [License](#license)
-   [References](#references)



## Introduction

The Speech to text converter (en) module is a data transformation component part of the Akimech solution in the AI Regio project, which involves several
cooperating modules for the speech-to-text and topic recognition tasks. The aim of this pipeline solution is to help industries in the mainenance processing.
This component has the aim to convert incoming audio files (binary files) into text.

![image](https://user-images.githubusercontent.com/103200695/171002111-c5e62748-9177-4bd0-bf17-0d3340e604d9.png)

This component is implemented as a GRPC server performing two sub-tasks: the segmentation of the audio file (if it is too long to be wholly processed) 
and the conversion from audio to text. 


## References

This component is based on the open source library "Speech Recognition": Zhang, A. (2017). Speech Recognition (Version 3.8) [Software]. 
Available from https://github.com/Uberi/speech_recognition#readme.
