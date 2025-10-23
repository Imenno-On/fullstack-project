import { useState } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { 
  ExternalLink, 
  Copy, 
  MoreVertical, 
  Trash2, 
  Edit,
  Users,
  Calendar,
  Check
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";

const mockTests = [
  {
    id: 1,
    title: "История России XX века",
    date: "15 октября 2025",
    link: "https://forms.yandex.ru/cloud/12345abcde/",
    students: 24,
    completed: 18,
    status: "active"
  },
  {
    id: 2,
    title: "Основы программирования на Python",
    date: "12 октября 2025",
    link: "https://forms.yandex.ru/cloud/67890fghij/",
    students: 32,
    completed: 32,
    status: "completed"
  },
  {
    id: 3,
    title: "Английская грамматика: Present Perfect",
    date: "10 октября 2025",
    link: "https://forms.yandex.ru/cloud/klmno12345/",
    students: 28,
    completed: 15,
    status: "active"
  },
  {
    id: 4,
    title: "Органическая химия: Углеводороды",
    date: "8 октября 2025",
    link: "https://forms.yandex.ru/cloud/pqrst67890/",
    students: 22,
    completed: 20,
    status: "active"
  },
  {
    id: 5,
    title: "Литература: Творчество Пушкина",
    date: "5 октября 2025",
    link: "https://forms.yandex.ru/cloud/uvwxy12345/",
    students: 26,
    completed: 26,
    status: "completed"
  },
  {
    id: 6,
    title: "Физика: Законы Ньютона",
    date: "2 октября 2025",
    link: "https://forms.yandex.ru/cloud/zabcd67890/",
    students: 30,
    completed: 12,
    status: "active"
  },
];

export function TestsPage() {
  const [tests, setTests] = useState(mockTests);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const handleCopy = (link: string, id: number) => {
    navigator.clipboard.writeText(link);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleDelete = (id: number) => {
    setTests(tests.filter((test) => test.id !== id));
  };

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-4 gap-6">
        <Card className="p-6 border-2 border-purple-100">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">Всего тестов</span>
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Check className="w-5 h-5 text-primary" />
            </div>
          </div>
          <p className="text-3xl font-semibold">{tests.length}</p>
        </Card>

        <Card className="p-6 border-2 border-green-100">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">Активные</span>
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <ExternalLink className="w-5 h-5 text-green-600" />
            </div>
          </div>
          <p className="text-3xl font-semibold">
            {tests.filter((t) => t.status === "active").length}
          </p>
        </Card>

        <Card className="p-6 border-2 border-blue-100">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">Учеников</span>
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Users className="w-5 h-5 text-blue-600" />
            </div>
          </div>
          <p className="text-3xl font-semibold">
            {tests.reduce((sum, test) => sum + test.students, 0)}
          </p>
        </Card>

        <Card className="p-6 border-2 border-yellow-100">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">Прохождений</span>
            <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
              <Calendar className="w-5 h-5 text-secondary" />
            </div>
          </div>
          <p className="text-3xl font-semibold">
            {tests.reduce((sum, test) => sum + test.completed, 0)}
          </p>
        </Card>
      </div>

      {/* Tests Grid */}
      <div className="grid grid-cols-2 gap-6">
        {tests.map((test) => (
          <Card key={test.id} className="p-6 hover:shadow-lg transition-shadow border-2 border-gray-100 hover:border-purple-200">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="font-semibold mb-2">{test.title}</h3>
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {test.date}
                  </span>
                  <span className="flex items-center gap-1">
                    <Users className="w-4 h-4" />
                    {test.completed}/{test.students}
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge
                  variant={test.status === "active" ? "default" : "secondary"}
                  className={
                    test.status === "active"
                      ? "bg-green-100 text-green-700 hover:bg-green-100"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-100"
                  }
                >
                  {test.status === "active" ? "Активен" : "Завершён"}
                </Badge>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <MoreVertical className="w-4 h-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>
                      <Edit className="w-4 h-4 mr-2" />
                      Редактировать
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      className="text-destructive"
                      onClick={() => handleDelete(test.id)}
                    >
                      <Trash2 className="w-4 h-4 mr-2" />
                      Удалить
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>

            {/* Progress bar */}
            <div className="mb-4">
              <div className="flex items-center justify-between text-sm mb-2">
                <span className="text-muted-foreground">Прогресс прохождения</span>
                <span className="font-medium">
                  {Math.round((test.completed / test.students) * 100)}%
                </span>
              </div>
              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary to-purple-600 rounded-full transition-all"
                  style={{ width: `${(test.completed / test.students) * 100}%` }}
                />
              </div>
            </div>

            {/* Link */}
            <div className="flex items-center gap-2 bg-accent border border-primary/20 rounded-lg p-3">
              <ExternalLink className="w-4 h-4 text-primary flex-shrink-0" />
              <a
                href={test.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-primary flex-1 truncate hover:underline"
              >
                {test.link}
              </a>
              <Button
                onClick={() => handleCopy(test.link, test.id)}
                variant="ghost"
                size="sm"
                className="flex-shrink-0 h-8 w-8 p-0"
              >
                {copiedId === test.id ? (
                  <Check className="w-4 h-4 text-green-600" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Empty state would go here if no tests */}
      {tests.length === 0 && (
        <Card className="p-12 text-center border-2 border-dashed border-gray-300">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <ExternalLink className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="font-semibold mb-2">Нет созданных тестов</h3>
          <p className="text-muted-foreground mb-6">
            Создайте свой первый тест с помощью AI
          </p>
          <Button className="bg-gradient-to-r from-primary to-purple-600">
            Создать тест
          </Button>
        </Card>
      )}
    </div>
  );
}
