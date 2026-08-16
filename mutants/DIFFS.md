# Diffs une ligne — mutants EN16931 1.3.16

Date : 16 Aug 2026 PT. Style `diff -u` (contexte / xpath). Une substitution par fichier.

## 1. CII_example1.xml — TOTAL (BT-112)

```diff
--- fixtures/CII_example1.xml
+++ mutants/CII_example1.xml
@@ rsm:SupplyChainTradeTransaction/ram:ApplicableHeaderTradeSettlement/ram:SpecifiedTradeSettlementHeaderMonetarySummation
-                <ram:GrandTotalAmount>250.33</ram:GrandTotalAmount>
+                <ram:GrandTotalAmount>250.34</ram:GrandTotalAmount>
```

L640. DuePayableAmount reste 250.33. Attendus : BR-CO-15, BR-CO-16.

## 2. CII_example3.xml — VAT (BT-117 vs BT-110)

```diff
--- fixtures/CII_example3.xml
+++ mutants/CII_example3.xml
@@ ram:ApplicableHeaderTradeSettlement/ram:ApplicableTradeTax
-                <ram:CalculatedAmount>225</ram:CalculatedAmount>
+                <ram:CalculatedAmount>226</ram:CalculatedAmount>
```

L111. `TaxTotalAmount` (BT-110) reste 225. Attendus : BR-CO-14, BR-S-09.

## 3. CII_example5.xml — MANDATORY (BT-1)

```diff
--- fixtures/CII_example5.xml
+++ mutants/CII_example5.xml
@@ rsm:ExchangedDocument/ram:ID   # BT-1 invoice number, PAS le ram:ID BT-24
-        <ram:ID>TOSL110</ram:ID>
+        <ram:ID></ram:ID>
```

L22. BT-24 (`GuidelineSpecifiedDocumentContextParameter/ram:ID`) inchangé. Attendu : BR-02.

## 4. CII_business_example_01.xml — LINE-SUM (BT-106)

```diff
--- fixtures/CII_business_example_01.xml
+++ mutants/CII_business_example_01.xml
@@ ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:LineTotalAmount
-                <ram:LineTotalAmount>1436.5</ram:LineTotalAmount>
+                <ram:LineTotalAmount>1436.51</ram:LineTotalAmount>
```

L473 (header). Somme des BT-131 de lignes inchangée. Attendus : BR-CO-10, BR-CO-13.

## 5. CII_business_example_02.xml — TYPE (BT-3)

```diff
--- fixtures/CII_business_example_02.xml
+++ mutants/CII_business_example_02.xml
@@ rsm:ExchangedDocument/ram:TypeCode
-        <ram:TypeCode>380</ram:TypeCode>
+        <ram:TypeCode>999</ram:TypeCode>
```

L20. 999 n'est pas dans UNTDID 1001. Attendu : BR-CL-01.

## 6. CII_business_example_Z.xml — ID-TRUNC (BT-31)

```diff
--- fixtures/CII_business_example_Z.xml
+++ mutants/CII_business_example_Z.xml
@@ ram:SellerTradeParty/ram:SpecifiedTaxRegistration/ram:ID[@schemeID='VA']
-          <ram:ID schemeID="VA">DE37/302/30168</ram:ID>
+          <ram:ID schemeID="VA">37</ram:ID>
```

L139. Tentative `→ DE37` : 0 failed-assert (FINDING, voir MUTANTS.md). Retenu : `37` → BR-CO-09.

## 7. CII-BR-CO-10-RoundingIssue.xml — MANDATORY (BT-24)

```diff
--- fixtures/CII-BR-CO-10-RoundingIssue.xml
+++ mutants/CII-BR-CO-10-RoundingIssue.xml
@@ ram:GuidelineSpecifiedDocumentContextParameter/ram:ID   # BT-24, PAS ExchangedDocument/ID (BT-1 = "0")
-            <ram:ID>urn:ferd:CrossIndustryDocument:invoice:1p0:comfort</ram:ID>
+            <ram:ID></ram:ID>
```

L10. Totaux nuls non touchés. Attendu : BR-01.

## 8. XRechnung-O.xml — DATE (BT-2)

```diff
--- fixtures/XRechnung-O.xml
+++ mutants/XRechnung-O.xml
@@ rsm:ExchangedDocument/ram:IssueDateTime/udt:DateTimeString
-      <udt:DateTimeString format="102">20210114</udt:DateTimeString>
+      <udt:DateTimeString format="102">20151399</udt:DateTimeString>
```

L23. Mois 13 / jour 99. BR-03 ne tire pas (présence). CII-DT-097 tire (regex YYYYMMDD).

## 9. ubl-tc434-creditnote1.xml — TOTAL UBL (BT-115)

```diff
--- fixtures/ubl-tc434-creditnote1.xml
+++ mutants/ubl-tc434-creditnote1.xml
@@ cac:LegalMonetaryTotal/cbc:PayableAmount
-		<cbc:PayableAmount currencyID="EUR">100.11</cbc:PayableAmount>
+		<cbc:PayableAmount currencyID="EUR">101.11</cbc:PayableAmount>
```

L108. TaxInclusiveAmount reste 100.11. Attendu : BR-CO-16.

## 10. huf_example_cii.xml — VAT-RATE (BT-119)

```diff
--- fixtures/huf_example_cii.xml
+++ mutants/huf_example_cii.xml
@@ ram:ApplicableHeaderTradeSettlement/ram:ApplicableTradeTax/ram:RateApplicablePercent
-				<ram:RateApplicablePercent>27.00</ram:RateApplicablePercent>
+				<ram:RateApplicablePercent>19.00</ram:RateApplicablePercent>
```

L325 (header BG-23 uniquement ; les 27.00 de lignes inchangés). CalculatedAmount 18679.00 inchangé. Attendus : BR-CO-17, BR-S-08, BR-S-09.
