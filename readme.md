## NLTK Libraries Required

Run the commands below:
```python
import nltk

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

```

## Troubleshooting Steps

#### `ERROR: Cannot install ... because these package versions have conflicting dependencies`

If the `requirements.txt` demands that that are requirements conflicts, simply relax the version constraints by removing the version numbers of the corresponding packages in `requirements.txt`


#### `ImportError: cannot import name 'cached_download' from 'huggingface_hub'`

- To fix this error, downgrade your version of huggingface_hub to an earlier version.
```python
pip install huggingface-hub==0.25.2
```

#### `Error "Microsoft Visual C++ 14.0 is required`

The methods below are equivalent. Once is cmd-line approach, the other is graphical approach.

Method 1:

`
vs_buildtools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
`


Method 2:

Install the [Visual Cpp Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)


Once it is executed, you will see the options to select:
Install 
- Desktop C++ Build Tools
- and on the bottom right tab, install MSVC VS2019 C++ BuildTools

https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst