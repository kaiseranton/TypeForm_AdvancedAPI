import requests

class CTypeForm:
	def __init__(self,apikey):
		self.apikey = apikey
		self.AUTH_URL = 'https://api.typeform.com'
		self.AUTH_HEADER = {'Authorization': 'Bearer ' + self.apikey}
		self.workspaces = None
	def getWorkspaces(self):
		if self.workspaces == None:
			self.WORKSPACES_FULLDATA = (requests.get(self.AUTH_URL + "/workspaces", headers=self.AUTH_HEADER)).json()
			self.WORKSPACES_ITEMS = self.WORKSPACES_FULLDATA['items']
			self.workspaces = list()
			for workspacetext in self.WORKSPACES_ITEMS:
				workspaceforms = (requests.get(self.AUTH_URL + "/workspaces/" + workspacetext['id'] + "/forms", headers=self.AUTH_HEADER)).json()['items']
				wspaceforms = list()
				for wform in workspaceforms:
					wspaceforms.append(CForm(wform['id'], wform['title'],wform['last_updated_at'], list()))
				workspace = CWorkspace(workspacetext['id'],workspacetext['name'],wspaceforms)
				self.workspaces.append(workspace)
		return self.workspaces
	def getWorkspaceByID(self,id):
		downloadData = (requests.get(self.AUTH_URL + "/workspaces/" + id, headers=self.AUTH_HEADER)).json()
		downloadDataForms = (requests.get(self.AUTH_URL + "/workspaces/" + id + "/forms", headers=self.AUTH_HEADER)).json()['items']
		downloadFormsList = list()
		for wform in downloadDataForms:
			downloadFormsList.append(CForm(wform['id'], wform['title'],wform['last_updated_at'], list()))
		return CWorkspace(downloadData['id'],downloadData['name'],downloadFormsList)
	def getFormResponse(self,form, indexfromchoice=False):
		downloadData = (requests.get(self.AUTH_URL + "/forms/" + form.getFormID() + "/responses?page_size=500", headers=self.AUTH_HEADER)).json()['items']
		returndata = list()
		for responsestring in downloadData:
			if indexfromchoice:
				if 'answers' in responsestring:
					for answerstring in responsestring['answers']:
						if 'choice' in answerstring:
							if 'label' in answerstring['choice']:
								for field in form.getFormFields():
									if field.getRef() == answerstring['field']['ref']:
										counter = 0
										for choi in field.getProperties()['choices']:
											if choi['label'] == answerstring['choice']['label']:
												answerstring['choice']['label'] = counter
											counter = counter + 1
			returndata.append(CResponse(responsestring))
		return returndata
	def getformByID(self,id):
		downloadData = (requests.get(self.AUTH_URL + "/forms/" + id, headers=self.AUTH_HEADER)).json()
		formfields = list()
		for field in downloadData['fields']:
			formfields.append(CFormField(field))
			if 'properties' in field:
				if 'fields' in field['properties']:
					for f2 in field['properties']['fields']:
						formfields.append(CFormField(f2))
		return CForm(downloadData['id'],downloadData['title'],"", formfields)
	
	
class CWorkspace:
	def __init__(self,id,name,forms):
		self.name = name
		self.id = id
		self.forms = forms
	def getID(self):
		return self.id
	def getName(self):
		return self.name
	def getForms(self):
		return self.forms
		
class CForm:
	def __init__(self,formID,title,last,formfields):
		self.formID = formID
		self.title = title
		self.last_updated_at = last
		self.formfields = formfields
	def getFormID(self):
		return self.formID
	def getTitle(self):
		return self.title
	def getLastUpdatedAt(self):
		return self.last_updated_at
	def getFormFields(self):
		return self.formfields
	def GetQuestionFromRef(self,id):
		for form in self.formfields:
			if form.getRef() == id:
				return form.getTitle()
		return ""
		

class CMetadata:
	def __init__(self,userdatastring):
		self.user_agent = userdatastring['user_agent'];
		self.platform = userdatastring['platform'];
		self.referer = userdatastring['referer'];
		self.network_id = userdatastring['network_id'];
		self.browser = userdatastring['browser'];
	def getUserAgent(self):
		return self.user_agent
	def getPlatform(self):
		return self.platform
	def getReferer(self):
		return self.referer
	def getNetworkID(self):
		return self.network_id
	def getBrowser(self):
		return self.browser

class CFormField:
	def __init__(self,fieldstring):
		self.id = fieldstring['id']
		self.type = fieldstring['type']
		self.ref = fieldstring['ref']
		self.title = fieldstring['title']
		self.properties = {}
		if 'properties' in fieldstring:
			self.properties = fieldstring['properties']
			
	def getID(self):
		return self.id
	def getType(self):
		return self.type
	def getRef(self):
		return self.ref
	def getTitle(self):
		return self.title
	def getProperties(self):
		return self.properties
class CAnswerField:
	def __init__(self,fieldstring):
		self.id = fieldstring['id']
		self.type = fieldstring['type']
		self.ref = fieldstring['ref']
	def getID(self):
		return self.id
	def getType(self):
		return self.type
	def getRef(self):
		return self.ref
		
class CAnswer:
	def __init__(self, answerstring):
		self.field = CAnswerField(answerstring['field'])
		self.type = answerstring['type']
		self.result = "UNKNOWNTYPE"
		if self.type == 'number':
			self.result = answerstring['number']
		if self.type == 'text':
			self.result = answerstring['text']
		if self.type == 'email':
			self.result = answerstring['email']
		if self.type == 'file_url':
			self.result = answerstring['file_url']
		if self.type == 'date':
			self.result = answerstring['date']
		if self.type == 'phone_number':
			self.result = answerstring['phone_number']
		if self.type == 'choice':
			if 'label' in answerstring['choice']:
				self.result = answerstring['choice']['label']
			else:
				self.result = answerstring['choice']['other']
		if self.type == 'choices':
			if 'labels' in answerstring['choices']:
				self.result = answerstring['choices']['labels']
			else:
				self.result = answerstring['choices']['others']
		if self.type == 'boolean':
			self.result = answerstring['boolean']
	def getField(self):
		return self.field
	def getType(self):
		return self.type
	def getResult(self):
		return self.result
		
class CResponse:
	def __init__(self,jsonstring):
		self.landing_id = jsonstring['landing_id']
		self.token = jsonstring['token']
		self.response_id = jsonstring['response_id']
		self.landed_at = jsonstring['landed_at']
		self.submitted_at = jsonstring['submitted_at']
		self.metadata = CMetadata(jsonstring['metadata'])
		self.answers = list()
		if 'answers' in jsonstring:
			for answerstring in jsonstring['answers']:
				self.answers.append(CAnswer(answerstring))
	def getLandingID(self):
		return self.landing_id
	def getToken(self):
		return self.token
	def getResponseID(self):
		return self.response_id
	def getLandedAt(self):
		return self.landed_at
	def getSubmittedAt(self):
		return self.submitted_at
	def getMetadata(self):
		return self.metadata
	def getAnswers(self):
		return self.answers
