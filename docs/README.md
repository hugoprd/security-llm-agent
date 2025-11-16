# PDFs para o RAG do Agente e seus conteúdos

**1. NIST SP 800-195**

Este PDF fala sobre as atividades de cibersegurança que o NIST realizou naquele ano. Esse relatório é uma exigência de uma lei americana chamada FISMA (Lei Federal de Gestão da Segurança da Informação).

**2. Common Vulnerability Scoring System v3.1: Specification Document**

O assunto principal é descrever o que é o CVSS: um sistema aberto usado para comunicar as características e a gravidade de vulnerabilidades de software. Ele explica a estrutura do CVSS, que é dividida em três grupos de métricas:

- Base: Qualidades intrínsecas da vulnerabilidade (que não mudam).
- Temporal: Características que mudam com o tempo (ex: se uma correção já existe).
- Ambiental: Características únicas do ambiente de um usuário específico.

**3. Common Vulnerability Scoring System v3.1: Examples**

O assunto é demonstrar como usar o sistema (descrito no Common Vulnerability Scoring System v3.1: Specification Document) para pontuar vulnerabilidades específicas. O documento fornece resumos de várias vulnerabilidades e mostra como pontuá-las.

**4. NIST Cybersecurity Framework (CSF)**

O PDF é um guia de melhores práticas para ajudar organizações a gerenciar seus riscos de cibersegurança.

Ele não é uma lei ou um padrão técnico obrigatório, mas sim uma estrutura voluntária que fornece uma "linguagem comum" para que todos na organização (desde a equipe técnica até a diretoria) possam entender, comunicar e gerenciar os riscos.

**5. Building a Vulnerability Management Program - A project management approach**

Este artigo examina o papel crítico do gerenciamento de projetos na construção de um programa de gerenciamento de vulnerabilidades bem-sucedido.

O artigo descreve como os riscos organizacionais e as necessidades de conformidade regulatória (compliance) podem ser abordados através de uma abordagem 'Plan-Do-Check-Act' (Planejar-Fazer-Verificar-Agir) aplicada ao programa de gerenciamento de vulnerabilidades.

**6. Vulnerability Management: Tools, Challenges and Best Practices**

Este artigo fala sobre a importância fundamental do Gerenciamento de Vulnerabilidades (Vulnerability Management - VM) para as empresas.

Ele explica que, no mercado atual, as empresas não podem se dar ao luxo de perder tempo, dinheiro ou integridade devido a incidentes de segurança, como:

- Interrupções na produção causadas por vírus ou worms.
- Um hacker desfigurar (defaces) um site.
- Informações críticas de clientes serem perdidas ou roubadas.

**7. A New Era in Vulnerability Management: A SANS Review of the Seemplicity Platform**

Esse artigo é uma análise interna feita por Dave Shackleford sobre uma plataforma chamada Seemplicity.

O Seemplicity é descrito como uma plataforma de orquestração de remediação (coordenação de correções) que:

- É agnóstica (independente) de fornecedor.
- Foi projetada para unificar o gerenciamento de vulnerabilidades em diferentes áreas: código, nuvem e infraestrutura.

**8. OWASP Top 10 para Aplicações de Modelo de Linguagem Grande (LLM) e IA Generativa**

O foco do artigo são os riscos de segurança específicos de sistemas que usam Inteligência Artificial, como chatbots e agentes de IA. Ele detalha as 10 vulnerabilidades mais críticas nessa área, incluindo:

- LLM01: Prompt Injection: Onde entradas do usuário podem alterar o comportamento do LLM de formas não intencionais.
- LLM07: System Prompt Leakage: Vazamento de instruções confidenciais do sistema (prompts do sistema).
- LLM08: Vector and Embedding Weaknesses: Fraquezas na forma como os vetores são gerados ou recuperados, especialmente em sistemas RAG (Retrieval-Augmented Generation).
- LLM06: Excessive Agency: Conceder ao LLM autonomia ou permissões excessivas para interagir com outros sistemas.

**9. Apresentação de agosto de 2022 do Centro de Coordenação de Cibersegurança do Setor de Saúde dos EUA (HC3)**

O PDF explica a lista OWASP Top 10 2021 "clássica", que se concentra nos riscos mais críticos para aplicações web em geral. O documento define o que é a fundação OWASP (Open Web Application Security Project)  e detalha cada uma das 10 vulnerabilidades da lista de 2021, como:

- A01:2021 - Broken Access Control (Quebra de Controle de Acesso) 
- A03:2021 - Injection (Injeção) 
- A05:2021 - Security Misconfiguration (Configuração Incorreta de Segurança) 
- A06:2021 - Vulnerable and Outdated Components (Componentes Vulneráveis e Desatualizados)

**10. OWASP Top 10 focada especificamente em segurança de APIs (Application Programming Interfaces)**

Ele explica que as APIs se tornaram um alvo principal para atacantes porque expõem a lógica do aplicativo e dados sensíveis. O documento detalha os 10 riscos mais críticos exclusivos das APIs, incluindo:

- API1:2019 - Broken Object Level Authorization (Quebra de Autorização em Nível de Objeto): Falha em verificar se um usuário tem permissão para acessar um objeto específico.
- API2:2019 - Broken User Authentication (Quebra de Autenticação de Usuário): Mecanismos de autenticação implementados incorretamente.
- API3:2019 - Excessive Data Exposure (Exposição Excessiva de Dados): Quando a API revela mais dados do que o necessário, deixando para o cliente a tarefa de filtrar informações sensíveis.
- API4:2019 - Lack of Resources & Rate Limiting (Falta de Recursos e Limitação de Taxa): Ausência de limites na quantidade de requisições, podendo levar a ataques de negação de serviço (DoS).