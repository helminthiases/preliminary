<br>

Missing Data Analysis, Exploratory Data Analysis

<br>

### The Programs

The statement/command

````shell
  python src/main.py
````

runs all the steps the table below outlines.

<br>

<table style="width: 65%; font-size: 65%; text-align: left; margin-left: 65px;">
    <colgroup>
        <col span="1" style="width: 30%;">
        <col span="1" style="width: 65%;">
        <col span="1" style="width: 5%;">
    </colgroup>
    <thead>
        <tr><th>action</th><th>comment</th><th><a href="./warehouse">storage:<br>warehouse/</a></th></tr>
    </thead>
    <tr>
        <td><ul>
            <li><a href=".src/missing/interface.py">src/missing/interface.py</a></li></ul></td>
        <td>The program's focus is null regression, i.e., it examines whether an independent variable's missing values 
            are predictable via <b>(a)</b> dependent variables, and <b>(b)</b> other independent variables.<br><br></td>
        <td><a href="./warehouse/missing">missing</a></td>
    </tr>
    <tr>
        <td><ul><li><a href=".src/cases/interface.py">src/cases/interface.py</a></li></ul></td>
        <td>Per country, and per geohelminth infection type, the program determines the number & proportion of observations 
            that are complete cases, i.e., have a year, co&ouml;rdinates, and infection type prevalence value.  The 
            <a href="https://helminthiases.github.io/data/missing.html#complete-cases">associated graphs</a> illustrate 
            the best data sets for modelling vis-&agrave;-vis minimal missing values.<br><br></td>
        <td><a href="./warehouse/cases">cases</a></td>
    </tr>
    <tr>
        <td><ul><li><a href=".src/explore/interface.py">src/explore/interface.py</a></li></ul></td>
        <td>The program creates data tables for interactive exploratory analysis via <a href="https://helminthiases.github.io/exploration" target="_blank">Tableau Public</a></td>
        <td><a href="./warehouse/explore">explore</a><br><br></td>
    </tr>
</table>


<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
