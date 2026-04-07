from setuptools import find_packages,setup
from typing import List

HYPEN_e_DOT="-e ."
def get_requirements(file_path:str)->List[str]: 
    '''
       this function returns list of package required to be install
    '''   
    requirements=[]  
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","")for req in requirements]

        if HYPEN_e_DOT in requirements:
            requirements.remove(HYPEN_e_DOT)
    
    return requirements
        

setup( #metatdata info about entire project
    name="ML_PROJECT",
    author="Kumudini",
    version="0.0.1",
    author_email="kumudinibudge@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)


"""
I’ll explain this **very simply and step-by-step** so the concept becomes clear. Think of this like how you would **explain it in an interview**.

---

# 1️⃣ First understand the basic idea

When you build a Python project like yours:

```
NetworkSecurity
│
├── networkSecurity
│   ├── pipeline
│   ├── utils
│   ├── component
│
├── setup.py
├── requirements.txt
```

Python **does not automatically know** that this whole project should behave like a **package**.

So you create **`setup.py`**.

👉 `setup.py` is a **project installer script**.

It tells Python:

* My project name is **NetworkSecurity**
* These are my **modules**
* These are the **libraries required**
* Install everything properly

---

# 2️⃣ What happens when you run

```
pip install -e .
```

Break this command:

| Part    | Meaning          |
| ------- | ---------------- |
| pip     | Python installer |
| install | install package  |
| -e      | editable mode    |
| .       | current project  |

So Python reads **setup.py** and installs your project.

---

# 3️⃣ Why we write `setup.py`

Without `setup.py` ❌

You cannot easily import your project modules.

Example problem:

```
from networkSecurity.pipeline.training_pipeline import TrainingPipeline
```

Python may say:

```
ModuleNotFoundError
```

Because Python doesn't know your project.

---

With `setup.py` ✅

After running:

```
pip install -e .
```

Your project becomes a **proper Python package**.

Now imports work anywhere.

---

# 4️⃣ What if we don't write setup.py?

Nothing will install automatically.

Problems:

❌ imports may fail
❌ dependencies not installed
❌ project cannot be reused
❌ cannot deploy project

---

# 5️⃣ What if we rename `setup.py`?

Example:

```
install.py
```

It **will NOT work**.

Because **pip only looks for `setup.py`**.

So the name **must be exactly `setup.py`**.

---

# 6️⃣ Now I will explain YOUR CODE

Your code:

```python
from setuptools import find_packages,setup
from typing import List
```

### Meaning

`setuptools`

Library used to **build Python packages**.

`find_packages`

Automatically finds folders containing Python modules.

Example it finds:

```
networkSecurity
networkSecurity.pipeline
networkSecurity.utils
networkSecurity.component
```

---

# 7️⃣ This line

```
HYPEN_e_DOT="-e ."
```

This is used because in **requirements.txt** sometimes we write:

```
pandas
numpy
scikit-learn
-e .
```

But `-e .` is **not a package**.

So we remove it.

---

# 8️⃣ This function

```
def get_requirements(file_path:str)->List[str]:
```

Purpose:

👉 Read **requirements.txt**
👉 Return list of libraries

Example `requirements.txt`

```
pandas
numpy
scikit-learn
```

Function returns:

```
["pandas","numpy","scikit-learn"]
```

---

# 9️⃣ Step-by-step working

### Step 1

Open file

```python
with open(file_path) as file_obj:
```

Open `requirements.txt`

---

### Step 2

Read lines

```python
requirements=file_obj.readlines()
```

Example result

```
["pandas\n","numpy\n","scikit-learn\n"]
```

---

### Step 3

Remove newline

```python
requirements=[req.replace("\n","")for req in requirements]
```

Now list becomes:

```
["pandas","numpy","scikit-learn"]
```

---

### Step 4

Remove `-e .`

```
if HYPEN_e_DOT in requirements:
    requirements.remove(HYPEN_e_DOT)
```

Because `-e .` is not a library.

---

# 🔟 Now the `setup()` function

```
setup(
    name="NetworkSecurity",
    author="Kumudini",
    version="0.0.1",
    author_email="kumudinibugde@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirement.txt')
)
```

This is **project information**.

---

### name

Project name

```
NetworkSecurity
```

---

### author

Project developer

```
Kumudini
```

---

### version

Project version

```
0.0.1
```

---

### packages

```
packages=find_packages()
```

This tells Python:

Find all modules inside project.

Example:

```
networkSecurity
networkSecurity.pipeline
networkSecurity.utils
networkSecurity.component
```

---

### install_requires

```
install_requires=get_requirements('requirement.txt')
```

This tells Python:

When installing this project, also install:

```
pandas
numpy
scikit-learn
```

---

# 1️⃣1️⃣ Example full workflow

Step 1

You run

```
pip install -e .
```

Step 2

Python reads **setup.py**

Step 3

It installs dependencies from **requirements.txt**

Step 4

Your project becomes importable

---

# 1️⃣2️⃣ Why `-e .` is used

`-e` means **editable mode**.

Editable means:

If you change code, you **don't need to reinstall project**.

Example:

You update

```
pipeline.py
```

Changes automatically work.

---

# 1️⃣3️⃣ Real-life example

Imagine you built a **calculator library**.

Without setup.py ❌

People cannot install it.

With setup.py ✅

People can run:

```
pip install calculator
```

---

# 1️⃣4️⃣ Best Interview Answer

If interviewer asks:

**What is the use of setup.py?**

Answer:

> setup.py is used to package the Python project and define metadata such as project name, version, dependencies, and modules. It allows the project to be installed using pip so that the modules can be imported and used across different environments.

---

✅ If you want, I can also explain **one extremely important concept related to setup.py** that **almost every ML interview asks**:

**Difference between**

```
pip install .
```

and

```
pip install -e .
```

This question appears in **90% ML engineer interviews**.

"""

