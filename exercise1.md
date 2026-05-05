# Exercise 1: Codes vs. Ciphers

A **code** operates at the level of words or phrases, replacing entire meaningful units with substitute words, numbers, or symbols according to a **codebook**. For example, a codebook might map "attack at dawn" to "7291" or "bridge" to "FALCON." Both parties must possess the same codebook to communicate. Codes are linguistically dependent—they work on semantic units—and their security relies on keeping the codebook secret.

A **cipher**, by contrast, operates at the level of individual characters (or bits/bytes), transforming them systematically using a **mathematical algorithm** and a **key**. For example, a Caesar cipher shifts each letter by a fixed number of positions in the alphabet. Ciphers are language-independent and can encrypt any data, not just predefined words. Their security relies on the secrecy of the key, not the algorithm (Kerckhoffs's principle).

In summary: codes substitute meaning-level units via lookup; ciphers transform individual symbols via algorithm and key.
