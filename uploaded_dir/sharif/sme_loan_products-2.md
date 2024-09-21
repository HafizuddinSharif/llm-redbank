# Loan Product Recommendation Logic

### 1. High Current Ratio (currat) & High Working Capital (workcap)

- **High Current Ratio:** currat > 2  
  **AND/OR**  
  **High Working Capital:** workcap > RM 200

**Product:**  
SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

**Purpose:**  
Property

**Reason (Short Version):**  
The customer has strong liquidity and excess working capital, suggesting the ability to efficiently manage short-term obligations. Property financing can help grow operations while utilizing this strong liquidity.

**Reason (Long Version):**  
The customer demonstrates a strong ability to cover short-term liabilities with current assets, indicating robust liquidity. This excess liquidity, combined with substantial working capital, positions the customer to pursue expansion or improvement. Property financing can leverage this strength to acquire or improve property assets, facilitating further business growth.

---

### 2. Low Current Ratio (currat) & Low Working Capital (workcap)

- **Low Current Ratio:** currat < 1  
  **AND/OR**  
  **Low Working Capital:** workcap < RM 50

**Product:**  
SME Quick Biz Financing – Biz Jamin, SME Biz Working Capital/-i

**Purpose:**  
Working Capital

**Reason (Short Version):**  
The customer is facing potential liquidity issues, requiring additional working capital to maintain day-to-day operations.

**Reason (Long Version):**  
A low current ratio may indicate struggles in meeting short-term obligations, leading to liquidity concerns. Combined with low working capital, external financing is urgently needed to stabilize operations. Products like SME Quick Biz Financing can provide the necessary funds for operational expenses, helping avoid disruptions.

---

### 3. Low Current Ratio (currat) & Low Working Capital (workcap) + Business in Listed Industries

- **Low Current Ratio:** currat < 1  
  **AND/OR**  
  **Low Working Capital:** workcap < RM 50  
  **AND**  
  **Listed Industries:** High Technology (Software, Aerospace, Bio-tech, etc.), Agriculture, Manufacturing, Tourism

**Product:**  
SME Quick Biz/-i GGSM

**Purpose:**  
Working Capital

**Reason (Short Version):**  
The customer faces liquidity issues and is eligible for the GSSM scheme due to their operation in industries like High Technology, Agriculture, Manufacturing, or Tourism.

**Reason (Long Version):**  
Customers operating in industries such as High Technology or Manufacturing with liquidity challenges may qualify for government-backed schemes like SME Quick Biz/-i GGSM. These sectors often face unique financial challenges, making specialized financing options essential for maintaining operations.

---

### 4. High Profit Margin (profit_margin) & High Return on Equity (return_on_equity)

- **High Profit Margin:** profit_margin > 10%  
  **AND**  
  **High ROE:** return_on_equity > 15

**Product:**  
SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

**Purpose:**  
Property or Working Capital

**Reason (Short Version):**  
Strong profitability and high returns suggest that the customer is well-positioned for massive growth and expansion.

**Reason (Long Version):**  
A high profit margin combined with a strong ROE indicates the customer is efficiently converting revenue into profit and generating substantial returns on shareholder investments. Financing for property or working capital can support expansion initiatives, allowing the customer to capitalize on their strong financial position.

---

### 5. Low Profit Margin (profit_margin) & High Gearing Ratio (gear)

- **Low Profit Margin:** profit_margin < 5%  
  **AND**  
  **High Gearing Ratio:** gear > 2

**Product:**  
SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

**Purpose:**  
Refinancing

**Reason (Short Version):**  
The customer has low profitability and high debt, suggesting a need for restructuring existing debt to improve financial stability.

**Reason (Long Version):**  
A low profit margin coupled with high gearing signals heavy reliance on debt financing, which can strain profitability. Refinancing existing debt through SME Biz Property Plus/i can help reduce interest costs and improve cash flow, stabilizing financial performance.

---

### 6. High Turnover Growth (turnover_growth) & High Profit Before Tax (plnpbt)

- **High Turnover Growth:** turnover_growth > 15%  
  **AND/OR**  
  **High Profit Before Tax:** plnpbt > RM 250  
  **AND**  
  **Low Total Assets:** totass < RM 2,500

**Product:**  
SME Quick Biz Financing – Biz Jamin, SME Biz Working Capital/-i

**Purpose:**  
Working Capital

**Reason (Short Version):**  
Rapid revenue growth combined with high PBT but low total assets suggests the customer is a startup in a niche market and may need additional capital to support rapid expansion.

**Reason (Long Version):**  
Rapid growth and significant profit, especially in businesses with limited assets, often indicate a startup in a niche market. Financing like SME Quick Biz can provide necessary working capital to support growth and meet increasing demand.

---

### 7. Low Turnover Growth (turnover_growth) & High Profit Before Tax (plnpbt)

- **Low Turnover Growth:** turnover_growth < 5%  
  **AND/OR**  
  **Low Profit Before Tax:** plnpbt < RM 150  
  **AND**  
  **High Total Assets:** totass > RM 5,000

**Product:**  
SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

**Purpose:**  
Property

**Reason (Short Version):**  
Low revenue growth and low PBT but high total assets suggest the customer is in a mature industry and may seek expansion opportunities.

**Reason (Long Version):**  
This combination indicates a mature business in a stable market. Property financing can help the customer diversify or expand by acquiring new properties, utilizing large assets as collateral.

---

### 8. Low Current Ratio (currat) & High Profit Margin (profit_margin)

- **Low Current Ratio:** currat < 1  
  **AND**  
  **High Profit Margin:** profit_margin > 10%

**Product:**  
SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100, SME Quick Biz Financing – Biz Jamin, SME Biz Working Capital/-i

**Purpose:**  
Working Capital

**Reason (Short Version):**  
Strong profitability but poor liquidity indicates the need for a short-term working capital loan to cover immediate liabilities.

**Reason (Long Version):**  
Despite strong profitability, poor liquidity suggests short-term cash flow challenges. A working capital loan can provide funds to meet immediate liabilities, allowing the business to maintain its growth trajectory without compromising long-term profitability.

---

### 9. Low Current Ratio (currat) & High Profit Margin (profit_margin) + Business in Listed Industries

- **Low Current Ratio:** currat < 1  
  **AND**  
  **High Profit Margin:** profit_margin > 10%  
  **AND**  
  **Listed Industries:** High Technology (Software, Aerospace, Bio-tech, etc.), Agriculture, Manufacturing, Tourism

**Product:**  
SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100, SME Quick Biz Financing – Biz Jamin, SME Biz Working Capital/-i

**Purpose:**  
Working Capital

**Reason (Short Version):**  
Strong profitability but poor liquidity in key industries may require specialized working capital financing to cover immediate liabilities.

**Reason (Long Version):**  
Businesses in specialized sectors like High Technology or Manufacturing with strong profitability but poor liquidity may benefit from government-backed schemes like SME Quick Biz to manage short-term cash flow challenges while growing in competitive markets.

---

### 10. High Gearing Ratio (gear) & Low Return on Equity (return_on_equity)

- **High Gearing Ratio:** gear > 2  
  **AND**  
  **Low ROE:** return_on_equity < 5%

**Product:**  
SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

**Purpose:**  
Refinancing

**Reason (Short Version):**  
High leverage with low ROE indicates over-leveraging, necessitating refinancing to reduce debt burden.

**Reason (Long Version):**  
A high gearing ratio with low ROE indicates over-reliance on debt without generating sufficient returns. Refinancing can help reduce debt, improve cash flow, and stabilize the business’s financial position.