import serpapi
import dotenv
import os
dotenv.load_dotenv()
def search(query:str)->str:
    print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")
    try:
        client = serpapi.Client(api_key=os.getenv("SERAPI_KEY"))
        params = {
            "engine": "google",
            "q": query,
            "location": "United States",
            "hl": "zh-cn",
            "gl": "cn",
        }
        results = client.search(params)
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if  "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and len(results["organic_results"]) > 0:
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n".join(snippets)
        return "No relevant information found."
    except Exception as e:
        return f"Error during search: {str(e)}"