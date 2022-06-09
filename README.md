<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/JohanHorsmans/Human-Computer-Interaction-2022">
    <img src="README_images/DJA_ICON.png" alt="Logo" width="151.25" height="103">
  </a>

  <h2 align="center">DJ Assistant</h2>

  <p align="center">
    Human Computer Interaction Exam Project 2022
    <br />
    <a href="https://github.com/JohanHorsmans/Human-Computer-Interaction-2022/blob/master/Human%20Computer%20Interaction%20Exam%20-%20Johan%20Horsmans%20-%20Final.pdf"><strong>Read the synopsis</strong></a>
    <br />
    <a href="https://github.com/JohanHorsmans/Human-Computer-Interaction-2022/blob/master/DJ_assistant.py">View main script</a>
    ·
    <a href="https://github.com/JohanHorsmans/Human-Computer-Interaction-2022/issues">Report bug</a>
    ·
    <a href="https://github.com/JohanHorsmans/Human-Computer-Interaction-2022/issues">Request feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the project</a>
    </li>
    <li>
      <a href="#getting-started">Getting started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About the project
There are many different factors one needs to consider when curating songs for a DJ set. Since songs need to be crossfaded into a continuous and uninterrupted stream of music, it is required that tracks have congruent tempo and keys while, simultaneously, complementing
each other aesthetically. Nonetheless, the amount of amateur DJs are on the rise and even most professionals are not trained in music theory. Followingly, these concepts can be difficult to relate to for a substantial portion of the DJ community.
The following repository presents a solution to this problem, namely, the DJ Assistant app, which allows users to get song recommendations that are congruent with a prespecified track on the aforementioned parameters.

**See <a href="https://github.com/JohanHorsmans/Human-Computer-Interaction-2022/blob/master/Human%20Computer%20Interaction%20Exam%20-%20Johan%20Horsmans%20-%20Final.pdf">```Human Computer Interaction Exam - Johan Horsmans - Final.pdf```</a> for the written synopsis.** The syniosis contains the theoretical and practical background behind the product as well as a thorough guide of different use cases and an
analysis of how various theories from the field of Human-Computer Interaction have been utilized and implemented in the UI. Lastly, the limitations and potential future prospects of DJ Assistant are discussed.

<!-- GETTING STARTED -->
## Getting started

To get a local copy up and running follow these simple steps:

**NOTE:** There may be slight variations depending on the terminal and operating system you use.  The following example is designed for Git Bash on macOS Monterey. You also need to have _pip_ installed:

### Prerequisites
For getting DJ Assistant up and running you need to clone the following repository and activate provided virtual environment. This can be done using the following lines in an unix-based bash:

```bash
git clone https://github.com/JohanHorsmans/Human-Computer-Interaction-2022.git
cd Human-Computer-Interaction-2022
bash create_venv.sh
source HCI_Exam/bin/activate
```

You should now be ready to run the code by running the following command in your python-editor of choice with the virtual environment activated:

```
streamlit run DJ_assistant.py
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b analysis/extended_analysis`)
3. Commit your Changes (`git commit -m 'Add some extended_analysis'`)
4. Push to the Branch (`git push origin analysis/extended_analysis`)
5. Open a Pull Request

<!-- LICENSE -->
## License
Distributed under the [MIT License](https://opensource.org/licenses/MIT). See ```LICENSE``` for more information.

<!-- CONTACT -->
## Contact

Feel free to write the author Johan Horsmans for any questions regarding the scripts.
You may do so through my email [Johan](mailto:201810219@post.au.dk)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
I would like to extend my gratitude towards the following:
* [Python](https://www.python.org/) - Software used for conducting the analysis.
* [Streamlit](https://docs.streamlit.io/) - Framework used for creating the app.
* [Spotify](https://www.spotify.com/us/) - For providing an available API.
* [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/#) - For providing a Python library for the Spotify Web API.
* [Overleaf](https://www.overleaf.com/) - Software used to format and write the report