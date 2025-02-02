# What is Truthlens

Truthlens is an analytic tool that allows users to upload a large dataset (in `csv` format). Users provide a dataset which they hope to analyse, which our application then uses for analysis - generating a credibility score and a visualisation of the topics and lexical similarities of the documents via a network graph.

It is hoped that such a tool will be helpful in both exploratory analyses and as a way for users to quickly categorize the documents which are useful to their topic of interest.

##  Features
- Upload CSV files (pdfs or links)
- Display processed data(through network graph)
- Analyse Data (through web scraping & pdf mining)
- Credibility rating



## Setup and Installation: 

Git clone the repository
```
git clone https://github.com/yourusername/your-repo.git
```
Create a virtual environment (optional but recommended):

Run ```python -m venv venv ```

## Activate Virtual Environment
Go to python `venv` folder



Run ```venv\Scripts\activate```


### Install dependencies
```
pip install -r requirements.txt
```
> If you <mark>face any issues during installation</mark>, refer to the section on troubleshooting below 

### Install required NLTK libraries

Run the commands below in a `python` prompt:
```python
import nltk

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')
```


### How to use:
Insert a dataset in the form of a `.csv` file. The `Text` column consists of a summarised version of the article - which could be from your favourite LLM such as DeepSeek or GPT-4. 

Your CSV file should be formatted as such:

If the dataset consists of PDFs, then the CSV should be formatted below as such:
| PDF Path |               Text              |
|----------|:-------------------------------:|
| 1.pdf    | Lorem ipsum dolor sit amet..... |
| 2.pdf    | Lorem ipsum dolor sit amet....  |

OR

If the dataset consists of News links, then the CSV should be formatted with columns below as such:
| Link                             |               Text              |
|----------------------------------|:-------------------------------:|
| https://www.channelnewsasia.com/ | Lorem ipsum dolor sit amet..... |
| https://edition.cnn.com/         | Lorem ipsum dolor sit amet....  |

Ensure that there are no trailing commas when saved as a csv file.

Lastly 😊: 

Run `venv\Scripts\activate`
Run `streamlit run Data_Visualisation.py`

###First Page
![First page](images\Upload files.png)



## Troubleshooting


#### `ERROR: Cannot install ... because these package versions have conflicting dependencies`

If the `requirements.txt` demands that that are requirements conflicts, simply relax the version constraints by removing the version numbers of the corresponding packages in `requirements.txt`


#### `ImportError: cannot import name 'cached_download' from 'huggingface_hub'`

- To fix this error, downgrade your version of huggingface_hub to an earlier version.
```python
pip install huggingface-hub==0.25.2
```

#### `Error "Microsoft Visual C++ 14.0 is required`

The methods below are equivalent. Once is cmd-line approach, the other is graphical approach.

**Method 1:**

```
vs_buildtools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
```

**Method 2:**

Install the [Visual Cpp Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)


Once it is executed, you will see the options to select:
Install 
- Desktop C++ Build Tools
- and on the bottom right tab, install MSVC VS2019 C++ BuildTools

https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst

