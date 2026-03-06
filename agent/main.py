import os
import sys
import re
from groq import Groq
from google import genai
from openai import OpenAI

ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "Bilinmeyen Görev")
ISSUE_BODY = os.environ.get("ISSUE_BODY", "Detay yok")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def parse_and_save_files(agent_response):
    """Yapay zekanın çıktısındaki dosyaları bulur ve fiziksel olarak oluşturur."""
    print("\n📂 Dosyalar taranıyor ve oluşturuluyor...")
    
    # [FILE: dosya/yolu.uzanti] formatını ve altındaki kod bloğunu yakalayan regex
    pattern = r"\[FILE:\s*(.+?)\]\s*```[a-zA-Z]*\n(.*?)\n```"
    matches = re.findall(pattern, agent_response, re.DOTALL)
    
    if not matches:
        print("⚠️ Uyarı: Çıktı içinde belirtilen formatta dosya bulunamadı.")
        return

    for file_path, file_content in matches:
        file_path = file_path.strip()
        # Eğer alt klasörler gerekiyorsa (örn: src/components) onları otomatik oluştur
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        # Dosyayı diske yaz
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        print(f"✅ Oluşturuldu: {file_path}")

def run_with_groq(prompt):
    print("🚀 Plan A: Groq (Llama 3.3) ile bağlanılıyor...")
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content

def run_with_gemini(prompt):
    print("🔄 Rate Limit! Plan B: Gemini API'ye geçiliyor...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def run_with_github_models(prompt):
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
    
    # Ajanı disipline eden yeni prompt. Dosyaları parse edebilmek için zorunlu kural ekledik.
    system_prompt = f"""
    Sen otonom bir AI yazılım mühendisisin.
    Şu an bir GitHub repousundasın ve aşağıdaki Issue'yu çözmen gerekiyor:
    
    Başlık: {ISSUE_TITLE}
    Detay: {ISSUE_BODY}
    
    Lütfen kodları üretirken KESİNLİKLE aşağıdaki katı formatı kullan. 
    Her yeni dosya için bu formatı tekrarla:
    
    [FILE: src/dosya_adi.js]
    ```javascript
    kodlar buraya gelecek
    ```
    """

    agent_response = ""

    try:
        agent_response = run_with_groq(system_prompt)
    except Exception as e:
        print(f"⚠️ Groq başarısız: {e}")
        try:
            agent_response = run_with_gemini(system_prompt)
        except Exception as e2:
            print(f"⚠️ Gemini başarısız: {e2}")
            try:
                agent_response = run_with_github_models(system_prompt)
            except Exception as e3:
                print(f"❌ Tüm API'ler çöktü! Hata: {e3}")
                sys.exit(1)

    print("\n🤖 Ajanın Ürettiği Çözüm:\n")
    print(agent_response)
    
    # Sihirli dokunuş: Loglanan kodları fiziksel dosyalara dönüştür
    parse_and_save_files(agent_response)

if __name__ == "__main__":
    main()