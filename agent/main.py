import os
import sys
import re
import subprocess
from groq import Groq
from google import genai
from openai import OpenAI
import time
import json

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
    
    cmd_results = []
    for cmd in commands:
        cmd = cmd.strip()
        print(f"🚀 Komut çalıştırılıyor: {cmd}")
        try:
            # Komutu çalıştır ve çıktıları yakala
            res = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True, env=os.environ)
            stdout = res.stdout or ""
            stderr = res.stderr or ""
            cmd_results.append((cmd, res.returncode, stdout, stderr))
            if res.returncode == 0:
                print(f"✅ Komut başarılı: {cmd}")
            else:
                print(f"⚠️ Komut hatası: {cmd} (kod {res.returncode})")
                print(stderr)
        except Exception as e:
            print(f"❌ Komut çalıştırılırken beklenmeyen hata: {cmd}\nDetay: {e}")
            cmd_results.append((cmd, -1, "", str(e)))

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
    return cmd_results

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
            
            # 1. Build Testi with retries and recovery
            def _run(cmd, retries=1, backoff=2, capture=True):
                attempt = 0
                while attempt < retries:
                    attempt += 1
                    print(f"🚀 Çalıştırılıyor (deneme {attempt}/{retries}): {cmd}")
                    if capture:
                        res = subprocess.run(cmd, shell=True, env=dict(os.environ, CI="true"), capture_output=True, text=True)
                    else:
                        res = subprocess.run(cmd, shell=True, env=dict(os.environ, CI="true"))
                    if res.returncode == 0:
                        return res
                    print(f"⚠️ Komut başarısız (kod {res.returncode}).")
                    if attempt < retries:
                        wait = backoff ** attempt
                        print(f"🔁 {wait}s sonra tekrar denenecek...")
                        time.sleep(wait)
                return res

            build_res = _run("npm run build", retries=3, capture=True)
            build_log = build_res.stdout + "\n" + build_res.stderr if hasattr(build_res, 'stdout') else ""
            if build_res.returncode != 0:
                print("❌ Build başarısız oldu, bağımlılıkları yeniden yükleyip bir deneme daha yapılıyor...")
                # Deneysel düzeltme adımları: önce paketleri yükle
                if os.path.exists("package-lock.json") or os.path.exists("npm-shrinkwrap.json"):
                    print("🔧 package-lock bulundu, 'npm ci' çalıştırılıyor...")
                    subprocess.run("npm ci --no-audit --prefer-offline", shell=True, env=os.environ)
                else:
                    print("🔧 package-lock bulunamadı, 'npm install' çalıştırılıyor...")
                    subprocess.run("npm install --no-audit --prefer-offline", shell=True, env=os.environ)

                # Son bir deneme daha
                build_res = _run("npm run build", retries=2, capture=True)
                build_log += "\n--- ikinci deneme ---\n" + (build_res.stdout + "\n" + build_res.stderr if hasattr(build_res, 'stdout') else "")
                if build_res.returncode != 0:
                    print("❌ KRİTİK HATA: Build tekrar başarısız oldu.")
                    # Hata düzeltilemedi; doğrulama başarısız
                    return False, build_log
            print("✅ Build başarılı.")

            # 2. Unit Test Kontrolü (Eğer script tanımlıysa)
            with open("package.json", "r") as f:
                content = f.read()
                if '"test":' in content and "no test specified" not in content:
                    print("🧪 Testler çalıştırılıyor...")
                    test_res = _run("npm test", retries=2, capture=True)
                    test_log = test_res.stdout + "\n" + test_res.stderr if hasattr(test_res, 'stdout') else ""
                    if test_res.returncode != 0:
                        print("❌ Uyarı: Testler başarısız oldu. Test bağımlılıkları veya test komutunu kontrol edin.")
                        return False, build_log + "\n--- test log ---\n" + test_log
                    print("✅ Tüm testler başarıyla geçti.")
                else:
                    print("⚠️ Test scripti bulunamadı, bu adım atlanıyor.")
        
        return True, build_log

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


def run_model(prompt):
    """Try available model endpoints in order and return the text. If all fail, return None."""
    try:
        return run_with_groq(prompt)
    except Exception as e:
        print(f"⚠️ Groq başarısız: {e}")
    try:
        return run_with_gemini(prompt)
    except Exception as e:
        print(f"⚠️ Gemini başarısız: {e}")
    try:
        return run_with_github_models(prompt)
    except Exception as e:
        print(f"⚠️ GitHub modelleri başarısız: {e}")
    return None


def compose_fix_prompt(prev_response, build_logs, attempt):
    return f"Aşağıdaki önceki ajan çıktısını ve build/test loglarını kullanarak ortaya çıkan hataları düzelt. Deneme #{attempt}. Önceki ajan çıktısı:\n{prev_response}\n\nBuild/Test Log:\n{build_logs}\n\nLütfen sadece [RUN:] ve [FILE:] formatında düzeltme adımlarını ver. Her denemede yapılan değişiklikleri kısa bir açıklama ile ekle." 

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
    agent_response = run_model(system_prompt)
    if not agent_response:
        print("❌ Tüm model çağrıları başarısız oldu. İşlem sonlandıruluyor.")
        return

    print("\n🤖 Ajanın Ürettiği Çözüm Uygulanıyor...\n")
    
    # 1. Adım: Dosyaları oluştur ve komutları çalıştır
    cmd_results = parse_and_execute(agent_response)

    # 2. Adım: Build ve Test Doğrulaması (PR Öncesi Filtre)
    # Ajanın oluşturduğu dizini tahmin et (örn: 'cd my-app' komutundan)
    project_dir = "."
    dir_match = re.search(r"\[RUN:\s*cd\s+([a-zA-Z0-9_-]+)", agent_response)
    if dir_match:
        project_dir = dir_match.group(1)

    is_valid, build_logs = verify_and_test(project_dir)

    MAX_FIX_ATTEMPTS = int(os.environ.get("MAX_FIX_ATTEMPTS", "5"))
    attempt = 0
    last_response = agent_response

    while not is_valid and attempt < MAX_FIX_ATTEMPTS:
        attempt += 1
        print(f"\n🔁 Hata tespit edildi — otomatik düzeltme denemesi {attempt}/{MAX_FIX_ATTEMPTS} başlıyor...")
        fix_prompt = compose_fix_prompt(last_response, build_logs, attempt)
        fix_response = run_model(fix_prompt)
        if not fix_response:
            print("❌ Model çağrıları başarısız oldu; daha fazla düzeltme denemesi yapılamıyor.")
            break

        # Uygula ve yeniden doğrula
        parse_and_execute(fix_response)
        is_valid, build_logs = verify_and_test(project_dir)
        last_response = fix_response

    if is_valid:
        print("\n✨ BAŞARI: Uygulama build edildi ve testleri geçti. PR aşamasına geçilebilir.")
    else:
        print("\n🛑 Uygulama hala build/test aşamasında hata veriyor. Tüm otomatik denemeler yapıldı.")
        print("ℹ️ İşlem sonlandırılıyor ama ajan çalışmayı bırakmayacak; elle müdahale gerekebilir.")
        return

if __name__ == "__main__":
    main()