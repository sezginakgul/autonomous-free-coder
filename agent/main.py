import os
import sys
import time
from groq import Groq
import google.generativeai as genai
from openai import OpenAI

# 1. GitHub Actions'tan gelen ortam değişkenlerini alıyoruz
ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "Bilinmeyen Görev")
ISSUE_BODY = os.environ.get("ISSUE_BODY", "Detay yok")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") # Plan C için GitHub Token

def run_with_groq(prompt):
    """Plan A: İşlemi çok hızlı olan Groq (Llama 3) ile yapmayı dener"""
    print("🚀 Plan A: Groq (Llama 3) ile bağlanılıyor...")
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192", 
    )
    return response.choices[0].message.content

def run_with_gemini(prompt):
    """Plan B: Groq limite takılırsa ücretsiz Gemini API'sine geçer"""
    print("🔄 Rate Limit! Plan B: Gemini API'ye geçiliyor...")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') 
    response = model.generate_content(prompt)
    return response.text

def run_with_github_models(prompt):
    """Plan C: İkisi de patlarsa GitHub Models (GPT-4o-mini) devreye girer"""
    print("🛡️ Çifte Limit! Plan C: GitHub Models API'sine geçiliyor...")
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=GITHUB_TOKEN,
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4o-mini", 
    )
    return response.choices[0].message.content

def main():
    print(f"🎯 Yeni Görev Alındı: {ISSUE_TITLE}")
    
    system_prompt = f"""
    Sen otonom bir AI yazılım mühendisisin.
    Şu an bir GitHub repousundasın ve aşağıdaki Issue'yu çözmen gerekiyor:
    
    Başlık: {ISSUE_TITLE}
    Detay: {ISSUE_BODY}
    
    Lütfen bu görevi yerine getirmek için hangi dosyalarda nasıl değişiklikler 
    yapılması gerektiğini adım adım açıkla ve kodları üret.
    """

    agent_response = ""

    # 3 Katmanlı Rate-Limit Koruması (Şelale Sistemi)
    try:
        if not GROQ_API_KEY:
            raise ValueError("Groq API Key eksik.")
        agent_response = run_with_groq(system_prompt)
        print("✅ Groq görevi başarıyla tamamladı!")
        
    except Exception as e:
        print(f"⚠️ Groq başarısız oldu: {e}")
        try:
            if not GEMINI_API_KEY:
                raise ValueError("Gemini API Key eksik.")
            agent_response = run_with_gemini(system_prompt)
            print("✅ Gemini görevi başarıyla tamamladı!")
            
        except Exception as e2:
            print(f"⚠️ Gemini de başarısız oldu: {e2}")
            try:
                if not GITHUB_TOKEN:
                    raise ValueError("GitHub Token eksik.")
                agent_response = run_with_github_models(system_prompt)
                print("✅ GitHub Models görevi kurtardı ve tamamladı!")
                
            except Exception as e3:
                print(f"❌ Tüm API'ler (Plan A, B, C) çöktü! Hata: {e3}")
                sys.exit(1)

    print("\n🤖 Ajanın Ürettiği Çözüm:\n")
    print(agent_response)

if __name__ == "__main__":
    main()