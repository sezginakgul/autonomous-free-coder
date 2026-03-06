import os
import sys
from groq import Groq
from google import genai
from openai import OpenAI

# 1. GitHub Actions'tan gelen ortam değişkenleri
ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "Bilinmeyen Görev")
ISSUE_BODY = os.environ.get("ISSUE_BODY", "Detay yok")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def run_with_groq(prompt):
    """Plan A: İşlemi güncel Groq (Llama 3.3) ile yapmayı dener"""
    print("🚀 Plan A: Groq (Llama 3.3) ile bağlanılıyor...")
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile", # Güncel model
    )
    return response.choices[0].message.content

def run_with_gemini(prompt):
    """Plan B: Google'ın yeni SDK'sı ve güncel modeli ile bağlanır"""
    print("🔄 Rate Limit! Plan B: Gemini API'ye geçiliyor...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Güncel model
        contents=prompt,
    )
    return response.text

def run_with_github_models(prompt):
    """Plan C: İkisi de patlarsa GitHub Models dener"""
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
    yapılması gerektiğini adım adım açıkla ve React kodlarını üret.
    """

    agent_response = ""

    # 3 Katmanlı Şelale Sistemi
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
                print("✅ GitHub Models görevi kurtardı!")
                
            except Exception as e3:
                print(f"❌ Tüm API'ler çöktü! Hata: {e3}")
                sys.exit(1)

    print("\n🤖 Ajanın Ürettiği Çözüm:\n")
    print(agent_response)

if __name__ == "__main__":
    main()