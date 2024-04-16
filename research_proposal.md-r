---
title:  "Research Proposal"
subtitle:  "Controllable, Reliable, and Safe Ingress Routing to the Cloud"
title-meta: ""
author: 
- name: "Jiangchen Zhu"
  affiliation: Columbia University
indent: true
documentclass: acmart
biblio-style: ACM-Reference-Format.bst
classoption:
- sigconf
- nonacm
- screen
- letterpaper
- 9pt
Biblio-style: ACM-Reference-Format.bst
header-includes:
- \pagestyle{plain}
---


\setlength{\footskip}{40pt}
\pagenumbering{arabic}



# Introduction
Clouds run numerous applications demanding low latency and high availability and serve clients from many geographically distributed \textit{sites}. To meet diverse objectives under fluctuating network conditions - such as reducing latency, load balancing between sites and routes, and ensuring fast failover during failures - the cloud needs complete and timely control over the routes its clients use to reach its sites, i.e., \textit{ingress routing} \tbd{cite}.


Two protocols are crucial for clients to reach the cloud: DNS and BGP. The clients first learn an IP address to access the cloud service (a DNS record) from the DNS server. When accessing the cloud, the packets destined to that address are sent along routes decided by BGP on the Internet. However, Both DNS and BGP have a number of known problems that make ingress routing control challenging.


DNS records are cached by clients' recursive resolvers, applications, and operating systems, which delays DNS updates on the client side. This hurts the cloud's availability when a previously cached IP address becomes unreachable due to failures. Each DNS record carries a time-to-live (TTL) value, determining how long a DNS record should be cached before expiring. Setting a low TTL causes clients to query the DNS server more frequently, which can slow down applications. Moreover, a shorter TTL value does not ensure timely DNS updates because many applications disrespect the TTL and continue using expired DNS records. Our analysis indicates that 13% of client connections are started after the DNS caches have expired, at median beginning 56 seconds after expiration. Specifically for cloud traffic, between 20-85% of traffic occurs more than a minute after the DNS TTL has expired.


BGP decides the path a client takes to access the cloud, but this decision is jointly made by the client network and others on the Internet, each following their own routing policies, thus being out of the cloud's control. BGP was not designed with the cloud's objectives, such as minimizing latency and load balancing, in mind, thus the absence of cloud's control over ingress routes leads to several issues. For instance, BGP may select routes with suboptimal performance, resulting in path inflation \cite{painter, anycast_matt, anycast_ppp, imc-jc-deanony, tango}. Moreover, load balancing becomes challenging when excessive clients converge on identical routes or target the same site \cite{tipsy, flavel2015fastroute}. BGP also suffers from convergence issues: BGP updates cause networks to reselect routes, potentially taking minutes to finalize their decisions, which results in higher packet loss and latency \cite{bgp-conv, a-measurement-study-on-the-impact}. Furthermore, rapidly updating BGP routing on a global scale contradicts operational best practices, as highlighted in a recent Google study \cite{capa}. Such operations are deemed *unsafe*, as any misconfiguration can quickly spread worldwide, triggering cascading failures. This significantly constrains the cloud's ability to safely respond to site failures. 


Though these limitations are longstanding, clouds still lack universally applicable and deployable solutions for controlling ingress routing. Systems like Google's Espresso and Facebook's EdgeFabric have been developed to optimize egress routes (from cloud to clients), demonstrating the significance of route selection control for cloud \cite{yap2017taking, schlinker2017engineering}. Controlling egress routes is relatively straightforward since the cloud itself makes the route decisions. In contrast, ingress route control remains challenging because it depends on client networks, which are outside the cloud's control. For ingress routing, two BGP announcement strategies, unicast (with DNS-based redirection) and anycast, are commonly utilized. However, these methods suffer from the limitations in DNS and BGP protocols. Specifically, unicast is hindered by DNS caching, which delays the failover of clients when a site fails. Anycast, on the other hand, compromises the cloud's control over which site clients are directed to, resulting in suboptimal performance and inadequate load balancing.


Some recent work improves ingress routing control but requires collaboration from customer networks or application developers. Systems such as PAINTER and TANGO can only be deployed at collaborative customer networks \cite{painter,tango-nsdi}. Solutions such as application-based redirect and multi-path transport protocols require application support, and their initial connection still uses DNS and BGP so their limitations still exist.


Moreover, studying cloud routing problems poses significant challenges for academic researchers, primarily because they lack the ability to test their routing solutions in real cloud networks on the real Internet. A typical cloud infrastructure spans tens to hundreds of sites worldwide, each connecting to hundreds of peers. While some testbeds enable researchers to conduct BGP routing experiments, their scope and scale fall short of faithfully emulating a cloud network \cite{tangled, schlinker19peering}. Conversely, simulating the Internet within a laboratory setting often fails to yield compelling results due to the complexities of accurately replicating both an accurate Internet topology and the networks' intricate routing policies, which are critical yet often undisclosed components of Internet routing \tbd{cite}.


My contributions have played a crucial role in advancing academic research on Internet routing at cloud scale and in the development of practical techniques to improve cloud ingress routing control, which were previously unattainable for cloud networks. These techniques adhere to existing Internet protocols and do not require external collaboration for easy deployment. Instead, they smartly leverage underutilized variables within these protocols that have rarely been considered in the context of cloud ingress routing.


\begin{itemize}[leftmargin=*]
    %\setlength{\itemindent}{-2\em}
\item


 \textbf{Expanding PEERING testbed to cloud scale} (\cref{sec:peering_vultr}). I collaborated with Vultr to expand PEERING \cite{schlinker19peering}, a BGP routing testbed, to cloud scale, enabling \textit{selective} BGP routing updates from 32 global locations to more than 5000 peers with customizable attributes such as AS path and BGP communities. This expansion makes realistic cloud routing research possible. For instance, a recent SIGCOMM paper leveraged this expanded testbed to develop and assess new ingress routing solutions for clouds \cite{painter}. Another study, recently published in NSDI, adopted a similar methodology, though researchers had to coordinate directly with the cloud provider to configure BGP \cite{tango-nsdi}. The expanded PEERING footprint is set to greatly simplify future research efforts in this field.


\item 
\textbf{Establishing fundamental tradeoffs in cloud ingress routing and developing techniques that achieve previously unattainable tradeoffs} (\cref{sec:pareto}). While the currently employed unicast and anycast techniques fall short of meeting certain objectives due to the limitations of DNS and BGP, it had been unclear whether a fundamental tradeoff is inherent in cloud ingress routing or if an "ideal" technique could exist. I proved an unavoidable tradeoff among control, availability, and operational safety in designing ingress routing solutions, a decision that must be tailored to a cloud's specific business needs. I then developed and evaluated new techniques that combine the strengths of existing methods, pushing them closer to the (unattainable) ideal.


\item 
\textbf{Achieving cloud routing objectives with higher ingress route control} (\cref{sec:community}).
I propose to develop new systems that take cloud's ingress routing objectives and network conditions as input to optimize the prefix announcement strategies from its sites. The objectives include minimizing the overall clients latency and load balancing between provider links. This requires the cloud to have rich ingress route control by tailoring where and to whom these announcements are made. Controlling what BGP route a directly neighboring network receives is straightforward, but influencing networks beyond a one-hop distance, where they are free to select from various BGP announcements they have learnt, is challenging. Fortunately, BGP communities allow the cloud to direct how neighboring networks further propagate its announcements, providing a mechanism by which the cloud can potentially further influence the routes of distant clients to increase its ingress control. \eat{ For example, the cloud can direct a neighboring network to suppress announcements to certain networks to encourage alternative routing paths.} However, the complexity of BGP communities, with their arbitrary formats and different types of actions documented on network-specific websites, makes manual interpretation and verification time-consuming and uncertain.  Automating the learning and verification of BGP communities is a critical first step towards providing more controlled ingress routing options to clients. Future challenges include assessing the benefit of a diverse set of ingress routes in achieving routing objectives and creating a scalable framework that integrates various BGP communities to optimize routing for many client networks. \eat{To effectively manage clients' ingress routes using BGP communities, a system first needs to predict the impact of specific BGP community actions, which vary widely (e.g., affecting one specific network or a set of networks, affecting global or regional networks). It must then correlate these predicted routes with specific objectives, such as minimizing client latency or balancing network load. The above processes require extensive measurements, including latency measurement and client preferences for various ingress routes. The final step involves searching among a vast set of potential ingress routing options to optimize the announcement strategy for each IP prefix to achieve the desired objectives. A practical method might involve a greedy algorithm, selecting the most beneficial BGP configuration update iteratively and stopping when additional changes yield marginal benefits.}




 
\end{itemize}



# Related Work
*Limitations of DNS.* One prior work shows how using DNS can control clients to specific sites, achieving ingress site control \cite{end-user-mapping}. Much has discussed the challenges of DNS TTL violation in cloud routing availability \cite{cache-me-if-you-can, dns-performance-caching, dns-in-context}.


*Limitations of BGP.*  





# Details of My Contributions
I aim to develop techniques that enable the cloud to meet its ingress routing objectives, such as improved latency and availability. Achieving these goals requires the cloud to have timely and flexible control over how external networks select their routes, a level of control that was previously unattainable without collaboration with them. To aid the research community in studying these routing challenges, I first upgraded a testbed to match the scale of a medium-sized cloud (\cref{sec:peering_vultr}). My proposed techniques continue to utilize existing Internet protocols, which allows for straightforward deployment. However, these techniques uniquely leverage underexplored variables within these protocols, enhancing their effectiveness (\cref{sec:pareto}, \cref{sec:community}).

## Expanding the PEERING Testbed
\label{sec:peering_vultr}
The PEERING testbed allows researchers to make customizable BGP announcements selectively to its neighboring networks, enhancing the study of BGP routing \cite{schlinker19peering}. Despite its utility in numerous innovative studies \cite{painter, imc-jc-deanony, vermeulen2022internet, anycast-agility, rtt-monitor}, PEERING's scale, 14 global locations and 5 IXP connections, is limited for routing studies with larger scale (e.g., cloud). Vultr, a cloud provider, enhances this by offering a "bring your own IP" service. This service lets its customers announce their IP spaces and choose which neighboring networks receive these announcements by tagging the relevant BGP communities. It also allows modification of attributes such as AS path and BGP communities in the BGP updates.


After integrating PEERING infrastructure with Vultr servers, researchers can now make BGP announcements from 32 additional locations, reaching over 5000 neighboring networks selectively. The expanded locations span several continents: 11 in North America, 2 in South America, 8 in Asia, 8 in Europe, 2 in Oceania, and 1 in Africa.


This expanded footprint provides a unique platform for addressing cloud routing challenges previously unexplored. A recent SIGCOMM paper utilized this enhanced testbed for cloud-enterprise collaborative routing studies \cite{painter}. The expanded capabilities can also retroactively enhance many studies that previously utilized the PEERING testbed \cite{imc-jc-deanony, anycast-agility}.

## Establishing Fundamental Tradeoffs in Cloud Ingress Routing and Developing Better Techniques
\label{sec:pareto}
The clouds have employed two strategies when routing their clients to their sites: unicast with DNS-based redirection and anycast. In unicast, each site announces a unique IP prefix and the DNS server returns clients an address within the prefix of a specific site to redirect the clients to that site. Despite the complete cloud control on clients redirection, the continued use of DNS caching after expiration makes quick DNS updates on client side impossible, delaying the failover when a site fails for minutes and losing availability.  On the other hand, in anycast, each site announces the same IP prefix, but the cloud compromises its *control* on which site a client will be routed to since the decision is made by the client networks and other networks instead of the cloud itself. Consequently, clients can end up being routed to geographically distant sites, experiencing increased latency. The lack of control also complicates load balancing between sites.


I define three key *goals* for cloud ingress routing: *control*, *availability* and *safety*. Control refers to the cloud's capability of routing clients to any site it wants. Availability refers to quickly rerouting clients from a failed site. Safety refers to avoiding updating BGP configurations on healthy sites to minimize the risk of cascading failure as quick global routing reconfiguration contradicts operational best practices. I first observe a fundamental tension: while control benefits from each site announcing a unique IP prefix, guaranteeing any packets destined to the prefix to arrive at the site, availability benefits from multiple sites announcing the same prefix, rerouting clients to healthy sites without waiting for the slow DNS update during site outage. Maximizing both control and availability requires changing BGP announcements upon site failure, compromising safety. I present a more formal proof in a recent submission.






Following this fundamental tradeoff, I develop and evaluate four techniques using the expanded PEERING testbed on the real Internet. \Cref{tab:summary} summarizes all comparisons among my proposed techniques with respect to CDN routing goals. The new techniques achieve previously unattainable combinations of goals, with no existing techniques that can beat them on one goal without compromising on another. Together, they form a new set of "best techniques" for CDN routing. The preliminary work on these techniques (with worse tradeoffs) was published in IMC and awarded a best short paper. The refined techniques are presented in a recently submitted paper.




\begin{table}[]
\small
\label{tab:summary}
\begin{tabular}{l|lll}
\multicolumn{1}{c|}{Technique}                 & Control                      & Availability                  & Safety                        \\ \hline
anycast                                        & {\color[HTML]{FE0000} low}   & {\color[HTML]{036400} high}   & {\color[HTML]{036400} high}   \\ \hline
unicast                                        & {\color[HTML]{036400} high}  & {\color[HTML]{FE0000} low}    & {\color[HTML]{036400} high}   \\ \hline
\eat{capacity-aware-proactive-superprefix} My technique A          & {\color[HTML]{036400} high}  & {\color[HTML]{FFCB2F} medium} & {\color[HTML]{036400} high}   \\ \hline
\eat{capacity-aware-safer-reactive-anycast} My technique B        & {\color[HTML]{036400} high}  & {\color[HTML]{036400} high}   & {\color[HTML]{FFCB2F} medium} \\ \hline
\eat{capacity-aware-controlled-proactive-prepending} My technique C & {\color[HTML]{036400} high-} & {\color[HTML]{036400} high-}  & {\color[HTML]{036400} high}   \\ \hline
\eat{capacity-aware-controlled-proactive-depref}  My technique D   & {\color[HTML]{036400} high-} & {\color[HTML]{036400} high}   & {\color[HTML]{036400} high}  
\end{tabular}
\caption{Ingress routing technique tradeoffs among three goals: control, availability and safety. Minus signs are used to indicate being slightly worse in achieving a certain goal. }
\label{tab:summary}




\end{table}



## Achieving Cloud Routing Objectives with Higher Ingress Route Control 
\label{sec:community}


While the techniques in \Cref{sec:pareto} manage to achieve the control on which *site* clients ingress the cloud without compromising much availability or safety, they have not yet achieved *ingress route* control. I plan to develop systems that take the cloud's routing objective as the input and decide how BGP routes are announced from each site. The objectives can vary from minimizing client latency overall or based on traffic priority, load balancing between links/paths, and facilitating failover after site/link outage. To achieve these objectives, cloud first needs rich control on the ingress route the clients take. Although it is straightforward to control the ingress routing for cloud's neighboring networks by making tailored announcements directly to them, it is hard to achieve this for many more networks that are beyond a one-hop distance since they are free to select any BGP routes learnt from other networks. 


Fortunately, the BGP community provides a powerful yet previously unexplored mechanism for influencing the routes of distant client networks. The cloud can direct how its directly neighboring networks further propagate its announcements to distant client networks by tagging the routes with tailored BGP communities. However, BGP communities are 32-bit values with arbitrary formats and network-specific interpretations documented on their websites. For example, two provider networks AS3257 and AS2914 have BGP communities with the same interpretation "do not announce to peers" but with drastically different values 65535:65284 and 2914:429. The types of actions encoded in BGP communities also vary significantly between networks. For example, 65501:nnn is a BGP community of AS2914 which means "prepend to a specific peer nnn 1x", allowing its customers to specify any peer network to apply the action. In contrast, the BGP communities from AS3491 do not support applying to any specific network, but instead have one particular value for each of its peer networks (e.g., 3491:60041 means "prepend to AS174 1x" and there are numerous other values for other networks).


Due to the diversity and a large volume of BGP communities, manual collection and interpretation of BGP communities is time-consuming and unscalable. Automating the learning and verification of BGP communities is the first challenge in realizing a system to achieve ingress route control. I have developed a set of techniques that leverage the latest developments in NLP tools to interpret the semantics of BGP communities and designed tailored Internet measurements to verify their interpretation. Here are the remaining challenges and planned milestones: 


To manage clients' ingress routes effectively using BGP communities, the system must first be capable of predicting the varied impacts of specific BGP community actions on clients' ingress routes. These can range widely - for example, some may target a single network while others affect multiple; some have global impacts, while others are regional. It then needs to align these predicted impacts with the objectives, such as minimizing client latency or load balancing between links and sites. The above processes demand extensive measurements to measure or predict route latencies as well as client networks' preferences for different exposable ingress routes. The next step involves searching among a vast set of potential ingress routing options to optimize the announcement strategy for each IP prefix to achieve the desired objectives. A practical method might involve a greedy algorithm, selecting the most beneficial BGP configuration update iteratively and stopping when additional changes yield marginal benefits.



# Conclusion
Existing routing techniques employed by the cloud are insufficient in achieving their routing objectives such as latency, load balancing and reliability, due to the limitations of DNS and BGP. The expansion of the PEERING testbed to cloud scale benefits my study of cloud ingress routing as well as the research community. I then propose and evaluate new techniques that significantly improve cloud's control over clients' ingress routes. My techniques for improving cloud ingress routing achieve previously unattainable tradeoffs and a fine-grained control. 












\iffalse

############## END OF PAPER #################
