import { useState } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Card } from "./ui/card";
import { Sparkles, ExternalLink, Copy, Check } from "lucide-react";

interface HomePageProps {
  onNavigate: (page: string) => void;
}

export function HomePage({ onNavigate }: HomePageProps) {
  const [inputText, setInputText] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedLink, setGeneratedLink] = useState("");
  const [copied, setCopied] = useState(false);

  const handleGenerate = () => {
    if (!inputText.trim()) return;
    
    setIsGenerating(true);
    // Имитация генерации
    setTimeout(() => {
      setGeneratedLink("https://forms.yandex.ru/cloud/12345abcde/");
      setIsGenerating(false);
    }, 2000);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-yellow-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-purple-600 rounded-xl flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-semibold">EduTest AI</span>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="ghost" onClick={() => onNavigate("dashboard")}>
              Мои тесты
            </Button>
            <Button onClick={() => onNavigate("auth")}>
              Войти
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-8 py-16">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 text-primary rounded-full mb-6">
            <Sparkles className="w-4 h-4" />
            <span className="text-sm">Powered by AI</span>
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-primary via-purple-600 to-primary bg-clip-text text-transparent">
            EduTest AI
          </h1>
          <p className="text-xl text-muted-foreground">
            Создавайте тесты из любого текста с помощью AI.
          </p>
        </div>

        {/* Input Section */}
        <Card className="p-8 shadow-xl border-2 border-purple-100">
          {!generatedLink ? (
            <div className="space-y-6">
              <div>
                <label className="block mb-3 text-foreground">
                  Вставьте текст для генерации теста
                </label>
                <Textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Например: История Российской Федерации началась после распада СССР в 1991 году. Первым президентом России стал Борис Ельцин..."
                  className="min-h-[300px] resize-none border-2 border-gray-200 focus:border-primary rounded-xl"
                />
              </div>
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>{inputText.length} символов</span>
                <span>Рекомендуемый объём: от 500 символов</span>
              </div>
              <Button
                onClick={handleGenerate}
                disabled={!inputText.trim() || isGenerating}
                className="w-full h-12 bg-gradient-to-r from-primary to-purple-600 hover:from-purple-600 hover:to-primary"
                size="lg"
              >
                {isGenerating ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Генерация теста...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2" />
                    Сгенерировать тест
                  </>
                )}
              </Button>
            </div>
          ) : (
            <div className="space-y-6 text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                <Check className="w-8 h-8 text-green-600" />
              </div>
              <div>
                <h3 className="text-2xl font-semibold mb-2">Тест успешно создан!</h3>
                <p className="text-muted-foreground mb-6">
                  Форма готова и опубликована в Яндекс Формах
                </p>
              </div>
              
              <div className="bg-accent border-2 border-primary/20 rounded-xl p-6">
                <p className="text-sm text-muted-foreground mb-3">Ссылка на форму:</p>
                <div className="flex items-center gap-3 bg-white border-2 border-primary/30 rounded-lg p-4">
                  <ExternalLink className="w-5 h-5 text-primary flex-shrink-0" />
                  <a 
                    href={generatedLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary flex-1 truncate hover:underline"
                  >
                    {generatedLink}
                  </a>
                  <Button
                    onClick={handleCopy}
                    variant="ghost"
                    size="sm"
                    className="flex-shrink-0"
                  >
                    {copied ? (
                      <Check className="w-4 h-4 text-green-600" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </Button>
                </div>
              </div>

              <div className="flex gap-3">
                <Button
                  onClick={() => {
                    setGeneratedLink("");
                    setInputText("");
                  }}
                  variant="outline"
                  className="flex-1"
                >
                  Создать новый тест
                </Button>
                <Button
                  onClick={() => onNavigate("dashboard")}
                  className="flex-1 bg-gradient-to-r from-primary to-purple-600"
                >
                  Перейти в кабинет
                </Button>
              </div>
            </div>
          )}
        </Card>

        {/* Features */}
        <div className="grid grid-cols-3 gap-6 mt-16">
          <Card className="p-6 text-center border-2 border-purple-100 hover:border-primary transition-colors">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-6 h-6 text-primary" />
            </div>
            <h4 className="font-semibold mb-2">AI генерация</h4>
            <p className="text-sm text-muted-foreground">
              Автоматическое создание вопросов на основе текста
            </p>
          </Card>
          <Card className="p-6 text-center border-2 border-yellow-100 hover:border-secondary transition-colors">
            <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <ExternalLink className="w-6 h-6 text-secondary" />
            </div>
            <h4 className="font-semibold mb-2">Яндекс Формы</h4>
            <p className="text-sm text-muted-foreground">
              Автоматическая публикация в Яндекс Формах
            </p>
          </Card>
          <Card className="p-6 text-center border-2 border-purple-100 hover:border-primary transition-colors">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Check className="w-6 h-6 text-primary" />
            </div>
            <h4 className="font-semibold mb-2">Быстро и просто</h4>
            <p className="text-sm text-muted-foreground">
              Создание теста за несколько секунд
            </p>
          </Card>
        </div>
      </main>
    </div>
  );
}
