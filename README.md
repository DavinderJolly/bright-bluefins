<!-- SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![pre-commit][pre-commit-shield]][pre-commit-url]
![python-version-shield]

<!-- PROJECT LOGO -->
<br>
<p align="center">
  <a href="https://github.com/DavinderJolly/bright-bluefins">
    <img src="docs/images/logo.png" alt="Logo" width="150" height="150">
  </a>
  <h1 align="center">BoxOS</h1>
  <br>
  <br>
  A fun Shell/REPL to mimic the nostalgic MS-DOS from the 1980's
  <br>
  <br>
</p>

<!-- TABLE OF CONTENTS -->

## Table of Contents

1. [About The Project](#about-the-project)
   - [Built With](#built-with)
1. [Getting Started](#getting-started)
   - [Installation on Windows](#Installation-on-Windows)
   - [Installation on Linux](#Installation-on-Linux)
1. [Usage](#usage)
1. [License](#license)
1. [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->

## About The Project

<p align="center">
    <img src="docs/images/App.png" alt="App screenshot">
</p> <br>

A clone of a 1980's MS-DOS built with python and prompt_toolkit framework.
This is a simplistic REPL with one of the most famous and basic commands of MS-DOS
and a basic text editor in-built like notepad.

### Built With

- [prompt_toolkit](https://pypi.org/project/prompt-toolkit/)
- [Pygments](https://pypi.org/project/Pygments/)
- [Pillow](https://pypi.org/project/Pillow/)
- [pythonping](https://pypi.org/project/pythonping/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Installation on Windows

1. Clone the repo
   ```sh
   git clone https://github.com/DavinderJolly/bright-bluefins.git
   ```
1. Install pipenv (skip to next step if already have it installed)

   ```sh
   py -m pip install pipenv
   ```

1. Install dependencies

   ```sh
   pipenv install
   ```

1. Start the program
   ```sh
   pipenv run start
   ```

### Installation on Linux

1. Clone the repo

   ```sh
   git clone https://github.com/DavinderJolly/bright-bluefins.git
   ```

1. Install pipenv (skip to next step if already have it installed)

   ```sh
   python -m pip install pipenv # (or python3 -m)
   ```

1. Install dependencies

   ```sh
   pipenv install
   ```

1. Start the program
   ```sh
   pipenv run start
   ```
   <!-- USAGE EXAMPLES -->

## Usage

A few of the famous commands are:

[ECHO](/docs/ShellCommands.md#echo)

```sh
ECHO Message
```

[EDIT](/docs/ShellCommands.md#edit)

```sh
EDIT filename.txt
```

[IMGVIEW](/docs/ShellCommands.md#imgview)

```sh
IMGVIEW image.png
```

[TREE](/docs/ShellCommands.md#tree)

```sh
TREE Path
```

[PING](/docs/ShellCommands.md#ping)

```sh
PING IP/domain
```

_For more examples, please refer to the [Documentation](https://example.com)_

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

- [Anonymous390](https://github.com/Anonymous390)
- [DavinderJolly](https://github.com/DavinderJolly)
- [Abir0](https://github.com/abir0)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-url]: https://github.com/DavinderJolly/bright-bluefins/graphs/contributors
[contributors-shield]: https://img.shields.io/github/contributors/DavinderJolly/bright-bluefins?style=flat
[issues-url]: https://github.com/DavinderJolly/bright-bluefins/issues
[issues-shield]: https://img.shields.io/github/issues/DavinderJolly/bright-bluefins?style=flat
[license-url]: https://github.com/DavinderJolly/bright-bluefins/blob/master/LICENSE.txt
[license-shield]: https://img.shields.io/github/license/DavinderJolly/bright-bluefins?style-flat
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[python-version-shield]: https://img.shields.io/github/pipenv/locked/python-version/DavinderJolly/Bright-Bluefins
