import os
import sys
import re
import subprocess
from groq import Groq
from google import genai
from openai import OpenAI

# Ortam Değişkenleri
ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "Bilinmeyen Görev")
ISSUE_BODY = os.environ.get("ISSUE_BODY", "Detay yok")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def parse_and_execute(agent_response):
    """Ajanın çıktısındaki hem terminal komutlarını hem de dosyaları işler."""
    
    # 1. Aşama: Terminal Komutlarını Yakala ve Çalıştır
    print("\n⚙️ Terminal komutları aranıyor ve çalıştırılıyor...")
    run_pattern = r"\[RUN:\s*(.+?)\]"
    commands = re.findall(run_pattern, agent_response)
    
    for cmd in commands:
        cmd = cmd.strip()
        print(f"🚀 Komut çalıştırılıyor: {cmd}")
        try:
            # Komutu gerçek Ubuntu terminalinde çalıştır
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ Komut başarılı: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Komut hatası: {cmd}\nDetay: {e}")

    # 2. Aşama: Dosyaları Yakala ve Diske Yaz
    print("\n📂 Dosyalar taranıyor ve oluşturuluyor...")
    file_pattern = r"\[FILE:\s*(.+?)\]\s*```[a-zA-Z]*\n(.*?)\n```"
    matches = re.findall(file_pattern, agent_response, re.DOTALL)
    
    if not matches:
        print("ℹ️ Çıktı içinde eklenecek yeni dosya bulunamadı.")
    
    for file_path, file_content in matches:
        file_path = file_path.strip()
        # Dosyanın dizinini oluştur
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        print(f"✅ Oluşturuldu/Güncellendi: {file_path}")

def verify_and_test(directory="."):
    """
    Uygulamanın build ve test süreçlerini kontrol eder.
    PR öncesi son güvenlik katmanıdır.
    """
    print("\n🔍 [DOĞRULAMA] Build ve Test süreçleri başlatılıyor...")
    
    # Mevcut çalışma dizinini sakla
    original_cwd = os.getcwd()
    
    try:
        # Eğer alt klasöre kurulum yapıldıysa oraya gir
        if directory != "." and os.path.exists(directory):
            os.chdir(directory)
            print(f"📂 Çalışma dizini değiştirildi: {directory}")

        # package.json varsa Node.js projesidir
        if os.path.exists("package.json"):
            print("📦 Bağımlılıklar ve Build kontrol ediliyor...")
            
            # 1. Build Testi
            build_res = subprocess.run("npm run build", shell=True, env=dict(os.environ, CI="true"))
            if build_res.returncode != 0:
                print("❌ KRİTİK HATA: Build başarısız oldu!")
                return False
            print("✅ Build başarılı.")

            # 2. Unit Test Kontrolü (Eğer script tanımlıysa)
            with open("package.json", "r") as f:
                content = f.read()
                if '"test":' in content and "no test specified" not in content:
                    print("🧪 Testler çalıştırılıyor...")
                    test_res = subprocess.run("npm test", shell=True, env=dict(os.environ, CI="true"))
                    if test_res.returncode != 0:
                        print("❌ KRİTİK HATA: Testler başarısız oldu!")
                        return False
                    print("✅ Tüm testler başarıyla geçti.")
                else:
                    print("⚠️ Test scripti bulunamadı, bu adım atlanıyor.")
        
        return True

    except Exception as e:
        print(f"⚠️ Doğrulama sırasında teknik hata: {e}")
        return False
    finally:
        # Her durumda ana dizine geri dön
        os.chdir(original_cwd)

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
        model='gemini-2.0-flash', # En güncel stabil sürüm
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
    
    system_prompt = f"""
    Sen otonom bir AI yazılım mühendisisin.
    Şu an bir GitHub repousundasın ve aşağıdaki Issue'yu çözmen gerekiyor:
    
    Başlık: {ISSUE_TITLE}
    Detay: {ISSUE_BODY}
    
    GÖREVLERİN:
    1. Eğer proje sıfırdan kurulacaksa, gerekli terminal komutlarını çalıştır.
    2. Kurulumdan sonra projenin içine girerek gerekli bileşenleri ve kodları oluştur.

    KURALLAR:
    - Terminal komutu için: [RUN: komut]
    - Dosya oluşturmak için: [FILE: yol/dosya.ext] ```kod```
    - Komutlar non-interactive (-y, --yes) olmalı.
    - ÖNEMLİ: PR açmadan önce mutlaka 'npm run build' ve varsa 'npm test' süreçlerini düşünerek kod yaz.
  KURALLAR (BUNLARA KESİNLİKLE UY):
    - Terminal komutu çalıştırmak için her komutu ayrı ayrı şu formatta yaz:
      [RUN: npm create vite@latest my-app -- --template react-ts]
      [RUN: cd my-app && npm install]
      [RUN: cd my-app && npm install tailwindcss]
    - Komutların etkileşimli (interactive) OLMAMASINA çok dikkat et. Kurulumların sorusuz geçmesi için --yes veya -y gibi bayraklar (flags) kullan.
    - Dosya oluşturmak için şu formatı kullan:
      [FILE: my-app/src/components/Button.tsx]
      ```tsx
      kodlar buraya
      ```
    - ÖNEMLİ: Eğer projeyi 'my-app' gibi bir alt klasöre kurduysan, dosya yollarının başına o klasörün adını eklemeyi unutma!
    - ÖNEMLİ: Terminal komutları ve dosya oluşturma işlemleri birbirinden bağımsızdır. Önce tüm terminal komutlarını çalıştır, ardından dosya oluşturma işlemlerine geç.
    - ÖNEMLİ: Sadece gerekli komutları ve dosyaları oluştur. Gereksiz veya fazladan adımlar atma.
    - ÖNEMLİ: Terminal komutları ve dosya oluşturma işlemleri sırasında ortaya çıkan hataları göz ardı etme. Hataları tespit eder etmez hemen düzeltmeye çalış. Hata düzeltme adımlarını da aynı formatta yaz.
    - ÖNEMLİ: Projede terminal komutları ve dosya oluşturma işlemleri arasında sık sık geçiş yapman gerekebilir. Her iki işlemi de birbirinden bağımsız olarak düşün ve sırayla uygula. Önce tüm terminal komutlarını çalıştır, ardından dosya oluşturma işlemlerine geç. Bu şekilde, her adımı net bir şekilde takip edebilir ve hataları daha kolay tespit edip düzeltebilirsin.
    - ÖNEMLİ: PR açmadan önce mutlaka Build ve Test süreçlerini tamamla. Eğer bu süreçlerde hata alırsan, hataları tespit edip düzeltmeye çalış. Hata düzeltme adımlarını da aynı formatta yaz.
       """

    agent_response = ""

    # Model Seçim Döngüsü
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

    print("\n🤖 Ajanın Ürettiği Çözüm Uygulanıyor...\n")
    
    # 1. Adım: Dosyaları oluştur ve komutları çalıştır
    parse_and_execute(agent_response)

    # 2. Adım: Build ve Test Doğrulaması (PR Öncesi Filtre)
    # Ajanın oluşturduğu dizini tahmin et (örn: 'cd my-app' komutundan)
    project_dir = "."
    dir_match = re.search(r"\[RUN:\s*cd\s+([a-zA-Z0-9_-]+)", agent_response)
    if dir_match:
        project_dir = dir_match.group(1)

    is_valid = verify_and_test(project_dir)

    if is_valid:
        print("\n✨ BAŞARI: Uygulama build edildi ve testleri geçti. PR aşamasına geçilebilir.")
    else:
        print("\n🛑 DURDURULDU: Uygulama build veya test aşamasında hata verdi. PR açılmayacak.")
        sys.exit(1)

if __name__ == "__main__":
    main()