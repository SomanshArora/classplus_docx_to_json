We need to create a webapp. 

The webapp will have a GUI interface and it will accept the docx file. 

The webapp will then convert the file into a xml. 

Webapp will read the xml and then traverse through all the tables mentioned in the xml. then convert the table data into a json format data.


We are expecting multiple tables in the document simlar to below structure. below is an example structure. 
<table>
  <thead>
    <tr>
      <td>Question</td>
      <td colspan="2">Which of the following explanations justifies for not placing hydrogen in either the group of alkali metals or halogens?</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Type</td>
      <td colspan="2">multiple_choice</td>
    </tr>
    <tr>
      <td>Option</td>
      <td>The ionization enthalpy of hydrogen is too high for group of alkali metals and too low for halogen group</td>
      <td>correct</td>
    </tr>
    <tr>
      <td>Option</td>
      <td>Hydrogen atom does not contain any neutron</td>
      <td>incorrect</td>
    </tr>
    <tr>
      <td>Option</td>
      <td>Hydrogen is much lighter than alkali metals or halogens</td>
      <td>incorrect</td>
    </tr>
    <tr>
      <td>Option</td>
      <td>Hydrogen can form compounds with almost all other elements.</td>
      <td>incorrect</td>
    </tr>
    <tr>
      <td>Solution</td>
      <td colspan="2">
        </td>
    </tr>
    <tr>
      <td>Marks</td>
      <td>1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>

we need to convert all of the tables into a json format like below example. 

{
  "question": "Which of the following explanations justifies for not placing hydrogen in either the group of alkali metals or halogens?",
  "type": "multiple_choice",
  "options": [
    {
      "text": "The ionization enthalpy of hydrogen is too high for group of alkali metals and too low for halogen group",
      "status": "correct"
    },
    {
      "text": "Hydrogen atom does not contain any neutron",
      "status": "incorrect"
    },
    {
      "text": "Hydrogen is much lighter than alkali metals or halogens",
      "status": "incorrect"
    },
    {
      "text": "Hydrogen can form compounds with almost all other elements.",
      "status": "incorrect"
    }
  ],
  "solution": "The solution is an image or rich text content.",
  "marks": {
    "correct": 1,
    "incorrect": 0
  }
}
