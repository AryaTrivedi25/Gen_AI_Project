from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import os



load_dotenv()

os.getenv("GROQ_API_KEY")

class Chain:
  def __init__(self):
    self.llm = ChatGroq(
      temperature = 0,
      groq_api_key = "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",
      model = "llama-3.1-70b-versatile"
    )
  
  def extract_jobs(self,cleaned_text):
    prompt_extract = PromptTemplate.from_template(
      """
      ### SCRAPED TEXT FROM WEBSITE :
      {page_data}
      ### INSTRUCTION :
      The scraped text is from the carrer's page of website.
      Your job is to extract the job postings and return them in JSON format containing 
      following keys : 'role', 'experience', 'skills' and 'description'.
      Only retur the valid JSON.
      ### VALID JSON (NO PREAMBLE):
      """
    )
    chain_extract = prompt_extract | self.llm
    try:
      res = chain_extract.invoke(input={'page_data': cleaned_text})
      print(f"LLM Response: {res.content}")  # Debug the raw LLM response
    except Exception as e:
      print(f"Error during LLM invocation: {e}")
      raise
    try:
      json_parser = JsonOutputParser()
      res = json_parser.parse(res.content)
    except OutputParserException:
      raise OutputParserException("Context too big. Unable to parse jobs.")
    return res if isinstance(res,list) else [res]
      
  def write_mail(self, job, links):
    prompt_email = PromptTemplate.from_template(
      """
      You are Arya Trivedi, a TNP student coordinator at Indian Institute of Information Technology, Surat. 
      IIIT Surat is an Institute of National Importance (INI) and a Government Funded Technical Institute (GFTI). 
      Your role involves facilitating placements and internships for students by connecting with companies. 
      Your task is to write a cold email to the client regarding the job mentioned above, 
      describing the capability of IIIT Surat students in fulfilling their needs.  
      Additionally, highlight the institute's achievements and the relevant programs that make students suitable for the role.  
      Include the most relevant details from the following links to showcase the institution's and student's strengths: {link_list}.  
      Remember, you are Arya Trivedi, TNP student coordinator at IIIT Surat.
      my Email id is "ui22cs10@iiitsurat.ac.in"
      my contact number is "+91 7016524856"
      Don not privide a preamble.
      ### Email (NO PREAMBLE):
      """
    )
    chain_email = prompt_email | self.llm
    res = chain_email.invoke({"job_description" : str(job), "link_list" : links})
    return res.content
    

if __name__ == "__main__":
  print(os.getenv("GROQ_API_KEY"))