# TypeForm_AdvancedAPI written in Python
## by Anton Kaiser

###### pip install typeform-advancedapi


Initialize
```
from typeform_advancedapi import *
API_KEY = ""
TypeForm = TypeForm_AdvancedAPI.CTypeForm(API_KEY)
```


Get Form
```
TypeForm.getformByID("XXXXXX")
```

Get Workspaces <-- returns an array with Workspace Objects
```
for workspace in TypeForm.getWorkspaces():
	print(workspace.getID())
	print(workspace.getName())
	for form in workspace.getForms():
		print(form.getFormID())
		print(form.getTitle())
```

Get Workspace by ID <-- returns the requested Workspace Object
```
workspaceobject = TypeForm.getWorkspaceByID("XXXXXXXX")
```

Get Form by ID <-- returns the Form Object
```
formobject = TypeForm.getformByID("XXXXXX")
```

Get Form by ID <-- returns the Form Object
```
responselist = TypeForm.getFormResponse(formobject)
OR
responselist = TypeForm.getFormResponse(formobject,true) <-- This will replace every choice answer with the index instead of the name
```

Objects:
```
CWorkspace:
getID() - Returns a String
getName() - Returns a String
getForms() - Returns a CForm array
```

```
CForm:
getFormID() - Returns a String
getTitle() - Returns a String
getLastUpdatedAt() - Returns a String
getFormFields() - Returns a CFormField Array
GetQuestionFromRef(QuestionREF) - Returns a String
```

```
CFormField:
getID() - Returns a String
getType() - Returns a String
getRef() - Returns a String
getTitle() - Returns a String
getProperties() - Returns a JSON Object

```

```
CResponse:
getLandingID() - Returns a String
getToken() - Returns a String
getResponseID() - Returns a String
getLandedAt() - Returns a String
getSubmittedAt() - Returns a String
getMetadata() - Returns a CMetadata Object
getAnswers() - Returns a CAnswer Array
```

```
CAnswer:
getField() - Returns a String
getType() - Returns a String
getResult() - Returns a String
```

```
CMetadata:
getUserAgent() - Returns a String
getPlatform() - Returns a String
getReferer() - Returns a String
getNetworkID() - Returns a String
getBrowser() - Returns a String
```

Example: Dumping Questions from a Form with QuestionID, Question
```
formID = "XXXXX"
form = TypeForm.getformByID(formID)
responselist = TypeForm.getFormResponse(form)
counter = 1
for answer in responselist[0].getAnswers():
	print(row.ExternalSurveyID + " Question " + str(counter) + "> " + answer.getField().getID() + " - " + form.GetQuestionFromRef(answer.getField().getRef()) + " | " + answer.getType())
	counter += 1
```