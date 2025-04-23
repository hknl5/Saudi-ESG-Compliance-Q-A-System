"use client"

import type React from "react"

import { useState } from "react"
import { Search, FileText, Settings, BookOpen, BarChart3, Globe, Shield, Info } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Slider } from "@/components/ui/slider"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"

export default function ESGComplianceAssistant() {
  const [query, setQuery] = useState("How do commercial banks incorporate ESG factors into their credit analysis?")
  const [isLoading, setIsLoading] = useState(false)
  const [answer, setAnswer] = useState("")
  const [sources, setSources] = useState<any[]>([])
  const [settings, setSettings] = useState({
    topResults: 3,
    enableReranking: true,
  })
  const [hasSearched, setHasSearched] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setIsLoading(true)
    setAnswer("")
    setSources([])

    // Simulate API call
    setTimeout(() => {
      setAnswer(
        "Commercial banks incorporate ESG factors into their credit analysis through a systematic and explicit inclusion of material ESG factors into traditional fundamental financial analysis. This is done by considering qualitative risks and opportunities, quantitative metrics, and incorporating ESG variables into models. These aspects collectively inform the bank's decision-making processes involved in proprietary investing and lending. This approach thus influences the way they assess the creditworthiness of borrowers.",
      )
      setSources([
        {
          id: 1,
          title: "commercial-banks-standard_en-gb.pdf",
          page: 12,
          excerpt:
            "The entity shall describe its approach to the incorporation of environmental, social and governance (ESG) factors in its credit analysis....",
          relevance: 0.8859,
        },
        {
          id: 2,
          title: "investment-banking-and-brokerage-standard_en-gb.pdf",
          page: 24,
          excerpt:
            "Integration of ESG factors is defined as the systematic and explicit inclusion of material ESG factors into traditional fundamental financial analysis...",
          relevance: 0.8833,
        },
        {
          id: 3,
          title: "commercial-banks-standard_en-gb.pdf",
          page: 31,
          excerpt: "5.1.4 Approach to incorporating ESG factors into assessing creditworthiness of borrowers...",
          relevance: 0.8809,
        },
      ])
      setIsLoading(false)
      setHasSearched(true)
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/20">
      <div className="container mx-auto px-4 py-8 max-w-5xl">
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-3">
            <Shield className="h-8 w-8 text-primary" />
            <h1 className="text-3xl font-bold tracking-tight">Smart ESG Compliance Assistant</h1>
          </div>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Ask any question about ESG regulations, standards, or best practices. Our AI will retrieve relevant
            information from trusted sources and provide accurate answers.
          </p>
        </header>

        <Card className="mb-8 border-primary/20 shadow-md">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-medium">Ask a question</CardTitle>
            <CardDescription>Enter your ESG-related question to get an accurate, sourced answer</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g., How do commercial banks incorporate ESG factors into their credit analysis?"
                  className="pl-10"
                />
              </div>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Searching..." : "Search"}
              </Button>
              <Sheet>
                <SheetTrigger asChild>
                  <Button variant="outline" size="icon" title="Search Settings">
                    <Settings className="h-4 w-4" />
                  </Button>
                </SheetTrigger>
                <SheetContent>
                  <SheetHeader>
                    <SheetTitle>Search Settings</SheetTitle>
                    <SheetDescription>
                      Customize how the assistant retrieves and processes information.
                    </SheetDescription>
                  </SheetHeader>
                  <div className="py-6 space-y-6">
                    <div className="space-y-2">
                      <Label htmlFor="top-results">Number of top results: {settings.topResults}</Label>
                      <Slider
                        id="top-results"
                        min={1}
                        max={10}
                        step={1}
                        value={[settings.topResults]}
                        onValueChange={(value) => setSettings({ ...settings, topResults: value[0] })}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <Label htmlFor="reranking" className="block">
                          Enable GPT reranking
                        </Label>
                        <p className="text-sm text-muted-foreground">Improve relevance with AI reranking</p>
                      </div>
                      <Switch
                        id="reranking"
                        checked={settings.enableReranking}
                        onCheckedChange={(checked) => setSettings({ ...settings, enableReranking: checked })}
                      />
                    </div>
                  </div>
                </SheetContent>
              </Sheet>
            </form>
          </CardContent>
        </Card>

        {isLoading && (
          <div className="flex flex-col items-center justify-center py-12">
            <div className="animate-pulse flex flex-col items-center">
              <BarChart3 className="h-12 w-12 text-primary/70 mb-4" />
              <h3 className="text-xl font-medium mb-2">Searching ESG Knowledge Base</h3>
              <p className="text-muted-foreground mb-4">Finding the most relevant information...</p>
              <Progress value={65} className="w-64 h-2" />
            </div>
          </div>
        )}

        {hasSearched && !isLoading && (
          <>
            <Tabs defaultValue="answer" className="mb-8">
              <TabsList className="mb-4">
                <TabsTrigger value="answer" className="flex items-center gap-2">
                  <BookOpen className="h-4 w-4" />
                  Answer
                </TabsTrigger>
                <TabsTrigger value="sources" className="flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  Sources ({sources.length})
                </TabsTrigger>
              </TabsList>

              <TabsContent value="answer">
                <Card className="border-primary/20 shadow-md">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-center">
                      <CardTitle>ESG Factors in Credit Analysis</CardTitle>
                      <Badge variant="outline" className="bg-primary/10 text-primary">
                        High Confidence
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="prose prose-green max-w-none">
                      <p className="leading-relaxed">{answer}</p>
                    </div>
                  </CardContent>
                  <CardFooter className="text-sm text-muted-foreground border-t pt-4 flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <Info className="h-4 w-4" />
                      <span>Answer generated from {sources.length} sources</span>
                    </div>
                    <Button variant="ghost" size="sm" className="gap-1">
                      <Globe className="h-3.5 w-3.5" />
                      <span>Learn More</span>
                    </Button>
                  </CardFooter>
                </Card>
              </TabsContent>

              <TabsContent value="sources">
                <div className="space-y-4">
                  {sources.map((source) => (
                    <Card key={source.id} className="overflow-hidden border-muted">
                      <CardHeader className="pb-2 bg-muted/30">
                        <div className="flex items-start justify-between">
                          <div>
                            <CardTitle className="text-base font-medium flex items-center gap-2">
                              <FileText className="h-4 w-4 text-primary" />
                              {source.title}
                            </CardTitle>
                            <CardDescription>Page {source.page}</CardDescription>
                          </div>
                          <div className="text-right">
                            <div className="flex items-center gap-1.5 mb-1">
                              <span className="text-sm font-medium">Relevance:</span>
                              <span className="text-sm font-bold text-primary">
                                {(source.relevance * 100).toFixed(1)}%
                              </span>
                            </div>
                            <Progress value={source.relevance * 100} className="w-24 h-1.5" />
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent className="pt-4">
                        <div className="pl-4 border-l-2 border-primary/30">
                          <p className="text-sm italic">{source.excerpt}</p>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
            </Tabs>

            <div className="bg-muted/30 rounded-lg p-4 border border-border">
              <h3 className="text-sm font-medium mb-2 flex items-center gap-2">
                <Info className="h-4 w-4 text-primary" />
                About ESG in Banking
              </h3>
              <p className="text-sm text-muted-foreground mb-3">
                Environmental, Social, and Governance (ESG) factors are increasingly important in the banking sector as
                financial institutions assess risks and opportunities in their lending and investment practices.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="bg-background rounded p-3 border border-border flex items-start gap-2">
                  <div className="bg-primary/10 p-1.5 rounded text-primary mt-0.5">
                    <BarChart3 className="h-4 w-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium">Systematic Integration</h4>
                    <p className="text-xs text-muted-foreground">
                      ESG factors are systematically included in financial analysis
                    </p>
                  </div>
                </div>
                <div className="bg-background rounded p-3 border border-border flex items-start gap-2">
                  <div className="bg-primary/10 p-1.5 rounded text-primary mt-0.5">
                    <Shield className="h-4 w-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium">Risk Assessment</h4>
                    <p className="text-xs text-muted-foreground">
                      Qualitative and quantitative ESG metrics inform risk models
                    </p>
                  </div>
                </div>
                <div className="bg-background rounded p-3 border border-border flex items-start gap-2">
                  <div className="bg-primary/10 p-1.5 rounded text-primary mt-0.5">
                    <Globe className="h-4 w-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium">Creditworthiness</h4>
                    <p className="text-xs text-muted-foreground">
                      ESG factors directly impact borrower creditworthiness evaluation
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
