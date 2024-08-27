## Financial Metrics available in CTOS xml:

turnover (Total Revenue)

plnpbt (Profit Before Tax)

plnpat (Profit After Tax)

turnover\_growth (Revenue Growth)

profit\_margin (Profit Margin)

return\_on\_equity (ROE)

currat (Current Ratio)

workcap (Working Capital)

gear (Gearing Ratio)

networth (Net Worth)

totass (Total Asset)

## Product Recommendation Logic

1. **High Current Ratio (currat) & High Working Capital (workcap)**

* High Current Ratio: currat \> 2.0  
  AND/OR  
* High Working Capital: workcap \> RM 200,000  
    
  Product: SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100  
    
  Purpose: Property  
    
  Reason (Short Ver): The customer has strong liquidity and excess working capital, suggesting the customer can efficiently manage its short-term obligations. Property financing can help it grow its operations and business while utilising the customer’s strong liquidity.

  Reason (Long Ver): The customer demonstrates a strong ability to cover short-term liabilities with current assets, indicating robust liquidity. This excess liquidity, combined with a substantial working capital buffer, positions the customer to pursue opportunities for expansion or improvement. Property financing, such as the SME Biz Property Plus/i, can help the customer leverage this strength to acquire or improve property assets, facilitating further business growth.

    
2. **Low Current Ratio (currat) & Low Working Capital (workcap)**

   * Low Current Ratio: currat \< 1.5  
     AND/OR  
     * High Working Capital: workcap \< RM 50,000

     
       Product: SME Quick Biz Financing – Biz Jamin, SME Biz Working Capital/-i

   

   Purpose: Working Capital

     
       Reason (Short Ver): The customer is facing potential liquidity issues, requiring additional working capital financing to maintain day-to-day operations.

   

   Reason (Long Ver): A low current ratio indicates that the customer may struggle to meet short-term obligations, potentially leading to liquidity issues. When combined with low working capital, this suggests an urgent need for external financing to stabilize operations. Products like SME Quick Biz Financing or SME Biz Working Capital/-i can provide the necessary working capital to cover working capital expenses such as purchase of inventory or operational expenses, helping the business avoid operational disruptions.

3. **Low Current Ratio (currat) & Low Working Capital (workcap) \+ \<type\_of\_business\> is any business considered under the listed industries**

   * Low Current Ratio: currat \< 1.5  
     AND/OR  
     * High Working Capital: workcap \< RM 50,000  
       AND  
     * Listed Industries: High Technology (Software, Aerospace, Bio-tech, Automotive, Nuclear Energy, Integrated Circuits, Computers, Microprocessors, etc.), Agriculture, Manufacturing, Tourism.

     
       Product: SME Quick Biz/-i GGSM

   

   Purpose: Working Capital

     
       Reason (Short Ver): The customer is facing potential liquidity issues, requiring additional working capital financing to maintain day-to-day operations. This customer is eligible for the special GSSM scheme because the customer operates in one of the following industries: High Technology, Agriculture, Manufacturing, Tourism.

       Reason (Long Ver): When a customer with liquidity challenges operates in industries such as High Technology, Agriculture, Manufacturing, or Tourism, they might qualify for government-backed schemes like SME Quick Biz/-i GGSM. These sectors often face unique financial challenges or opportunities, making them eligible for specialized financing options that provide working capital support, helping them navigate sector-specific risks and maintain their operations.

4. **High Profit Margin (profit\_margin) & High Return on Equity (return\_on\_equity)**

   * High Profit Margin: profit\_margin \> 10%  
     AND  
     * High ROE: return\_on\_equity \> 15

     
       Product: SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

   

   Purpose: Property or Working Capital

     
       Reason (Short Ver): Strong profitability and high returns suggest that the customer is well-positioned for massive growth and expansion.

       Reason (Long Ver): A high profit margin combined with a strong ROE indicates that the customer is efficiently converting revenue into profit and generating substantial returns on shareholder investments. This financial health suggests that the business is well-managed and ripe for growth. Property or working capital financing can support expansion initiatives, allowing the customer to capitalize on their strong financial position.

   

5. **Low Profit Margin (profit\_margin) & High Gearing Ratio (gear)**

   * Low Profit Margin: profit\_margin \< 5%  
     AND  
     * High Gearing Ratio: gear \> 2.0

     
       Product: SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

   

   Purpose: Refinancing

     
       Reason (Short Ver): The customer is potentially suffering a low level of profitability coupled with high debt, suggesting the need for restructuring existing debt to improve financial stability.

   

   Reason (Long Ver): A low profit margin coupled with a high gearing ratio, signals that the customer is heavily reliant on debt financing, which can strain profitability. Refinancing existing debt through products like SME Biz Property Plus/i can help reduce interest costs and improve cash flow, enabling the business to stabilize its financial position and potentially enhance profitability.

6. **High Turnover Growth (turnover\_growth) & High Profit Before Tax (plnpbt)**

   * High Turnover Growth: turnover\_growth \> 15%  
     AND/OR  
     * High Profit Before Tax: plnpbt \> RM 250,000  
       AND  
     * Low Total Assets: totass \< RM 2,500,000

     
       Product: SME Quick Biz Financing – Biz Jamin, SME Biz Working Capital/-i

   

   Purpose: Working Capital

     
       Reason (Short Ver): Rapid revenue growth combined with high PBT but low total assets suggests that the customer is a startup in a niche/emerging market and may need additional capital to sustain and support its rapid expansion.

       Reason (Long Ver): Rapid revenue growth and significant profit before tax, especially in a business with limited total assets, suggest a startup or early-stage company that is scaling quickly. These businesses often require additional working capital to sustain their growth trajectory and meet increasing demand. Financing products like SME Quick Biz Financing – Biz Jamin can provide the necessary capital to support continued expansion and increasing working capital expenses.

7. **Low Turnover Growth (turnover\_growth) & High Profit Before Tax (plnpbt)**

   * Low Turnover Growth: turnover\_growth \< 5%  
     AND/OR  
     * Low Profit Before Tax: plnpbt \< RM 150,000  
       AND  
     * High Total Assets: totass \> RM 5,000,000

     
       Product: SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

   

   Purpose: Property

     
       Reason (Short Ver): Low revenue growth combined with low PBT but high total assets suggests that the customer is in a mature industry. The customer may look towards expansion opportunities.

   

   Reason (Long Ver): A combination of low revenue growth and substantial profit before tax in a company with large total assets typically indicates a mature business in a stable, possibly saturated, market. These companies may be looking for ways to diversify or expand, making property financing an attractive option since they have a lot of assets to be able to be collateralised. Products like SME Biz Property Plus/i can facilitate the acquisition of new properties to support expansion efforts or increase operational efficiency.

8. **Low Current Ratio (currat) & High Profit Margin (profit\_margin)**

   * Low Current Ratio: currat \< 1.5  
     AND  
     * High Profit Margin: profit\_margin \> 10%

     
       Product: SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100, SME Quick Biz Financing – Biz Jamin, SME Biz Working Capital/-i

   

   Purpose: Working Capital

     
       Reason (Short Ver): Strong profitability but poor liquidity indicates that the customer may need a short-term working capital loan to cover immediate liabilities.

   

   Reason (Long Ver): Strong profitability with poor liquidity indicates that the customer is generating sufficient revenue but may be facing short-term cash flow challenges. In this scenario, a working capital loan can bridge the gap, providing the necessary funds to meet immediate liabilities without sacrificing long-term profitability. This ensures the business can continue to operate smoothly while maintaining its growth trajectory.

9. **Low Current Ratio (currat) & High Profit Margin (profit\_margin) \+ \<type\_of\_business\> is any business considered under the listed industries**

   * Low Current Ratio: currat \< 1.5  
     AND  
     * High Profit Margin: profit\_margin \> 10%  
       AND  
     * Listed Industries: High Technology (Software, Aerospace, Bio-tech, Automotive, Nuclear Energy, Integrated Circuits, Computers, Microprocessors, etc.), Agriculture, Manufacturing, Tourism.

     
       Product: SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100, SME Quick Biz Financing – Biz Jamin, SME Biz Working Capital/-i

   

   Purpose: Working Capital

     
       Reason (Short Ver): Strong profitability but poor liquidity indicates that the customer may need a short-term working capital loan to cover immediate liabilities.

   

   Reason (Long Ver): Similar to the general low current ratio and high profit margin scenario, but focused on businesses in key industries like High Technology, Agriculture, Manufacturing, or Tourism. These sectors often require specialized support due to their unique operating conditions. The combination of strong profitability and poor liquidity in these industries suggests that the business may benefit from targeted financing options, such as those available through SME Quick Biz Financing or government-backed schemes, to manage short-term cash flow while continuing to grow in a competitive market.

10. **High Gearing Ratio (gear) & Low ROE (return\_on\_equity)**

    * High Gearing Ratio: gear \> 2.0  
      AND  
      * Low ROE: return\_on\_equity \< 5%

      
        Product: SME Biz Property Plus/i, SME Biz Property Plus Extra/i, SME Biz Property Plus/i 100

    

    Purpose: Refinancing

      
        Reason (Short Ver): High leverage with low returns on equity indicates that the customer may be over-leveraged, needing a refinancing solution to reduce its debt burden.

    

    Reason (Long Ver): The reason for recommending refinancing in this scenario is that a high gearing ratio combined with a low return on equity suggests the customer is highly leveraged but is not generating sufficient returns on their equity. This situation often indicates that the company is struggling to effectively use its capital to generate profits, which can lead to financial instability. Refinancing can help by restructuring the company's existing debt to potentially lower interest rates or extend repayment periods, thereby alleviating some of the financial pressure and improving overall financial health.

