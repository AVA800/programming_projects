package com.customerregistration.entity;

import com.customerregistration.enums.*;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Table(name="loanapplicants")
@Getter
@Setter
public class Customer {
    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
    private Long Customer_ID;
    private Integer Dependents;
    private Integer Applicant_Income;
    private Integer Coapplicant_Income;
    private Integer Loan_Amount;
    private Integer Loan_Amount_Term;
    private Integer Credit_History;

    @Enumerated(EnumType.STRING)
    private Education Education;

    @Enumerated(EnumType.STRING)
    private Gender Gender;

    @Enumerated(EnumType.STRING)
    private LoanStatus Loan_Status;

    @Enumerated(EnumType.STRING)
    private Married Married;

    @Enumerated(EnumType.STRING)
    private PropertyArea Property_Area;

    @Enumerated(EnumType.STRING)
    private SelfEmployed Self_Employed;
}