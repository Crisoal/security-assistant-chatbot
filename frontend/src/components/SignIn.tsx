import React from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";

// Define TypeScript types
interface SignInFormData {
  email: string;
  password: string;
}

// Validation schema using Yup
const signinSchema = yup.object().shape({
  email: yup.string().email("Invalid email").required("Email is required"),
  password: yup
    .string()
    .min(6, "Password must be at least 6 characters")
    .required(),
});

const SignIn: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignInFormData>({
    resolver: yupResolver(signinSchema),
  });

  const onSubmit = (data: SignInFormData) => {
    console.log("Signin Data:", data);
    alert("Signin successful! 🚀");
  };

  return (
    <div className="auth-container">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input type="email" placeholder="Email" {...register("email")} />
        <p className="error">{errors.email?.message}</p>

        <input
          type="password"
          placeholder="Password"
          {...register("password")}
        />
        <p className="error">{errors.password?.message}</p>

        <button type="submit">Sign In</button>
      </form>
    </div>
  );
};

export default SignIn;
